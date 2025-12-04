from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.exceptions import BadRequestError, NotFoundError
from models.instrument import Instrument
from models.reagent import Reagent
from models.reaction import Reaction
from models.scenario import Scenario
from models.scenario_step import ScenarioStep
from services.reaction import _generate_reaction_key, get_required_reagents_for_reaction
from services.utils import validate_instrument_reagent_compatibility


class AmountUnit(str, Enum):
    GRAM = "g"
    MILLILITER = "mL"
    DROP = "drop"


@dataclass
class ContainerMeta:
    instrument_id: int
    instrument_type: str
    is_container: bool
    allowed_physical_states: Optional[str] = None


@dataclass
class ContainerContentItem:
    reagent_id: int
    amount_value: float
    amount_unit: str


@dataclass
class ScenarioRunState:
    run_id: str
    scenario_id: int
    containers: Dict[str, List[ContainerContentItem]]
    containers_meta: Dict[str, ContainerMeta]
    current_step_index: int = 0
    message: Optional[str] = None


# In-memory store for active runs
_runs: Dict[str, ScenarioRunState] = {}


def _default_containers_meta(db: Session) -> Dict[str, ContainerMeta]:
    meta: Dict[str, ContainerMeta] = {}

    beakers = (
        db.query(Instrument)
        .filter(Instrument.instrument_type == "beaker", Instrument.is_container.is_(True))
        .order_by(Instrument.id)
        .all()
    )
    if beakers:
        meta["beaker_1"] = ContainerMeta(
            instrument_id=beakers[0].id,
            instrument_type="beaker",
            is_container=True,
            allowed_physical_states=beakers[0].allowed_physical_states,
        )
    if len(beakers) > 1:
        meta["beaker_2"] = ContainerMeta(
            instrument_id=beakers[1].id,
            instrument_type="beaker",
            is_container=True,
            allowed_physical_states=beakers[1].allowed_physical_states,
        )

    flasks = (
        db.query(Instrument)
        .filter(Instrument.instrument_type == "flask", Instrument.is_container.is_(True))
        .order_by(Instrument.id)
        .all()
    )
    if flasks:
        meta["flask_1"] = ContainerMeta(
            instrument_id=flasks[0].id,
            instrument_type="flask",
            is_container=True,
            allowed_physical_states=flasks[0].allowed_physical_states,
        )

    pipette = (
        db.query(Instrument)
        .filter(Instrument.instrument_type == "pipette")
        .order_by(Instrument.id)
        .first()
    )
    if pipette:
        meta["pipette_1"] = ContainerMeta(
            instrument_id=pipette.id,
            instrument_type="pipette",
            is_container=False,
            allowed_physical_states=pipette.allowed_physical_states,
        )

    spatula = (
        db.query(Instrument)
        .filter(Instrument.instrument_type == "spatula")
        .order_by(Instrument.id)
        .first()
    )
    if spatula:
        meta["spatula_1"] = ContainerMeta(
            instrument_id=spatula.id,
            instrument_type="spatula",
            is_container=False,
            allowed_physical_states=spatula.allowed_physical_states,
        )

    if not meta:
        raise NotFoundError("Nenhum instrumento encontrado para inicializar a simulação.")

    return meta


def _state_to_dict(state: ScenarioRunState) -> Dict[str, object]:
    return {
        "run_id": state.run_id,
        "scenario_id": state.scenario_id,
        "current_step_index": state.current_step_index,
        "containers": {
            name: [asdict(item) for item in contents]
            for name, contents in state.containers.items()
        },
        "containers_meta": {name: asdict(meta) for name, meta in state.containers_meta.items()},
        **({"message": state.message} if state.message else {}),
    }


def start_scenario_run(scenario_id: int, db: Session) -> Dict[str, object]:
    run_id = str(uuid.uuid4())
    containers_meta = _default_containers_meta(db)
    containers: Dict[str, List[ContainerContentItem]] = {name: [] for name in containers_meta}
    state = ScenarioRunState(
        run_id=run_id,
        scenario_id=scenario_id,
        containers=containers,
        containers_meta=containers_meta,
        current_step_index=0,
    )
    _runs[run_id] = state
    return _state_to_dict(state)


def _get_state(run_id: str) -> ScenarioRunState:
    if run_id not in _runs:
        raise NotFoundError("Execução do cenário não encontrada.")
    return _runs[run_id]


def get_run_state(run_id: str, db: Session | None = None) -> Dict[str, object]:
    state = _get_state(run_id)
    return _state_to_dict(state)


def _get_ordered_steps_for_scenario(db: Session, scenario_id: int) -> list[ScenarioStep]:
    scenario = db.get(Scenario, scenario_id)
    if not scenario:
        raise NotFoundError("Cenário não encontrado.")
    return sorted(list(scenario.steps), key=lambda s: s.order_index)


def _get_current_step(db: Session, state: ScenarioRunState) -> ScenarioStep | None:
    steps = _get_ordered_steps_for_scenario(db, state.scenario_id)
    if state.current_step_index >= len(steps):
        return None
    return steps[state.current_step_index]


def _does_action_match_step(
    action_type: str,
    instrument_id: int | None,
    source_container_name: str | None,
    target_container_name: str | None,
    reagent_id: int | None,
    amount_value: float | None,
    amount_unit: str | None,
    step: ScenarioStep,
) -> bool:
    if action_type != step.action_type:
        return False

    if step.instrument_id is not None and instrument_id != step.instrument_id:
        return False

    if step.reagent_id is not None and reagent_id != step.reagent_id:
        return False

    if step.source_container_name is not None and source_container_name != step.source_container_name:
        return False

    if step.target_container_name is not None and target_container_name != step.target_container_name:
        return False

    if step.amount_value is not None and amount_value != step.amount_value:
        return False

    if step.amount_unit is not None and amount_unit != step.amount_unit:
        return False

    return True


def add_reagent_to_container(
    db: Session, run_id: str, container_name: str, reagent_id: int
) -> Dict[str, object]:
    return apply_action(
        run_id=run_id,
        action_type="add_reagent",
        instrument_id=None,
        source_container_name=None,
        target_container_name=container_name,
        reagent_id=reagent_id,
        amount_value=1.0,
        amount_unit="un",
        db=db,
    )


def _ensure_container_meta(state: ScenarioRunState, container_name: str) -> ContainerMeta:
    container_meta = state.containers_meta.get(container_name)
    if not container_meta:
        raise BadRequestError("O recipiente informado é inválido para esta simulação.")
    if not container_meta.is_container:
        raise BadRequestError("Este instrumento não pode ser usado como recipiente.")
    return container_meta


def _apply_reaction_if_matches(
    db: Session,
    state: ScenarioRunState,
    container_name: str,
) -> None:
    contents = state.containers.get(container_name, [])
    container_reagents = {item.reagent_id for item in contents}
    if not container_reagents:
        state.message = None
        return

    candidates = (
        db.query(Reaction)
        .filter(
            or_(Reaction.scenario_id == state.scenario_id, Reaction.scenario_id.is_(None)),
        )
        .all()
    )

    applicable: list[tuple[int, Reaction]] = []
    for reaction in candidates:
        required = get_required_reagents_for_reaction(reaction)
        if required and required.issubset(container_reagents):
            applicable.append((len(required), reaction))

    if not applicable:
        state.message = None
        return

    applicable.sort(key=lambda x: x[0], reverse=True)
    reaction = applicable[0][1]

    total_amount = sum(item.amount_value for item in contents if item.amount_value is not None)
    unit = next((item.amount_unit for item in contents if item.amount_unit), "un")

    required_ids = get_required_reagents_for_reaction(reaction)
    state.containers[container_name] = [
        item for item in contents if item.reagent_id not in required_ids
    ]
    state.containers[container_name].append(
        ContainerContentItem(
            reagent_id=reaction.product_reagent_id,
            amount_value=total_amount if total_amount else 1.0,
            amount_unit=unit,
        )
    )
    state.message = reaction.message


def _add_content(
    state: ScenarioRunState,
    container_name: str,
    reagent_id: int,
    amount_value: float,
    amount_unit: str,
) -> None:
    contents = state.containers.setdefault(container_name, [])
    for item in contents:
        if item.reagent_id == reagent_id and item.amount_unit == amount_unit:
            item.amount_value += amount_value
            return
    contents.append(
        ContainerContentItem(
            reagent_id=reagent_id,
            amount_value=amount_value,
            amount_unit=amount_unit,
        )
    )


def _remove_content(
    contents: List[ContainerContentItem],
    reagent_id: int,
    amount_value: float,
    amount_unit: str,
) -> None:
    for item in contents:
        if item.reagent_id == reagent_id and item.amount_unit == amount_unit:
            if item.amount_value < amount_value:
                raise BadRequestError("Não há quantidade suficiente deste reagente no recipiente de origem.")
            item.amount_value -= amount_value
            if item.amount_value == 0:
                contents.remove(item)
            return
    raise BadRequestError("Não há quantidade suficiente deste reagente no recipiente de origem.")


def apply_action(
    run_id: str,
    action_type: str,
    instrument_id: int | None,
    source_container_name: str | None,
    target_container_name: str | None,
    reagent_id: int | None,
    amount_value: float | None,
    amount_unit: str | None,
    db: Session,
) -> Dict[str, object]:
    state = _get_state(run_id)
    unit_value = amount_unit.value if isinstance(amount_unit, AmountUnit) else amount_unit
    unit_value_str = str(unit_value) if unit_value is not None else None

    steps = _get_ordered_steps_for_scenario(db, state.scenario_id)
    current_step = _get_current_step(db, state)
    if current_step is None:
        raise BadRequestError("Este cenário já foi concluído. Não há mais passos a realizar.")

    if not _does_action_match_step(
        action_type=action_type,
        instrument_id=instrument_id,
        source_container_name=source_container_name,
        target_container_name=target_container_name,
        reagent_id=reagent_id,
        amount_value=amount_value,
        amount_unit=unit_value_str,
        step=current_step,
    ):
        raise BadRequestError("Essa ação não corresponde ao passo atual do cenário.")

    if action_type == "add_reagent":
        if reagent_id is None or target_container_name is None or amount_value is None or unit_value_str is None:
            raise BadRequestError("Dados insuficientes para adicionar reagente.")
        container_meta = _ensure_container_meta(state, target_container_name)
        instrument = db.get(Instrument, container_meta.instrument_id)
        if not instrument:
            raise NotFoundError("Instrumento não encontrado para este recipiente.")
        reagent = db.get(Reagent, reagent_id)
        if not reagent:
            raise NotFoundError("Reagente não encontrado.")
        validate_instrument_reagent_compatibility(instrument, reagent)
        _add_content(state, target_container_name, reagent_id, amount_value, unit_value_str)
        _apply_reaction_if_matches(db, state, target_container_name)
        state.current_step_index += 1
        state.message = f"Passo concluído: {current_step.text_instruction}"
        return _state_to_dict(state)

    if action_type == "transfer_solid_with_spatula":
        if instrument_id is None:
            raise BadRequestError("Instrumento é obrigatório para esta ação.")
        instrument = db.get(Instrument, instrument_id)
        if not instrument or instrument.instrument_type != "spatula":
            raise BadRequestError("Instrumento informado não é uma espátula válida.")
        if reagent_id is None or target_container_name is None:
            raise BadRequestError("Recipiente de destino e reagente são obrigatórios.")
        if amount_value is None or unit_value_str is None:
            raise BadRequestError("Quantidade e unidade são obrigatórias para esta ação.")
        if unit_value_str != AmountUnit.GRAM.value:
            raise BadRequestError("A unidade para transferência com espátula deve ser g.")
        unit_value_str = AmountUnit.GRAM.value

        reagent = db.get(Reagent, reagent_id)
        if not reagent:
            raise NotFoundError("Reagente não encontrado.")
        if reagent.physical_state != "solid":
            raise BadRequestError("A espátula só pode ser usada com reagentes sólidos.")
        validate_instrument_reagent_compatibility(instrument, reagent)

        if source_container_name is None:
            _ensure_container_meta(state, target_container_name)
            _add_content(state, target_container_name, reagent_id, amount_value, unit_value_str)
            _apply_reaction_if_matches(db, state, target_container_name)
            state.current_step_index += 1
            state.message = f"Passo concluído: {current_step.text_instruction}"
            return _state_to_dict(state)

        source_meta = _ensure_container_meta(state, source_container_name)
        target_meta = _ensure_container_meta(state, target_container_name)
        _ = source_meta, target_meta

        source_contents = state.containers.setdefault(source_container_name, [])
        _remove_content(source_contents, reagent_id, amount_value, unit_value_str)
        _add_content(state, target_container_name, reagent_id, amount_value, unit_value_str)
        _apply_reaction_if_matches(db, state, target_container_name)
        state.current_step_index += 1
        state.message = f"Passo concluído: {current_step.text_instruction}"
        return _state_to_dict(state)

    if action_type == "transfer_liquid_with_pipette":
        if instrument_id is None:
            raise BadRequestError("Instrumento é obrigatório para esta ação.")
        instrument = db.get(Instrument, instrument_id)
        if not instrument or instrument.instrument_type != "pipette":
            raise BadRequestError("Instrumento informado não é uma pipeta válida.")
        if reagent_id is None or target_container_name is None:
            raise BadRequestError("Recipiente de destino e reagente são obrigatórios.")
        if amount_value is None or unit_value_str is None:
            raise BadRequestError("Quantidade e unidade são obrigatórias para esta ação.")
        if unit_value_str not in {AmountUnit.MILLILITER.value, "drop"}:
            raise BadRequestError("A unidade para transferência com pipeta deve ser mL ou gotas.")
        unit_value_str = unit_value_str

        reagent = db.get(Reagent, reagent_id)
        if not reagent:
            raise NotFoundError("Reagente não encontrado.")
        if reagent.physical_state not in {"liquid", "solution"}:
            raise BadRequestError("A pipeta só pode ser usada com líquidos ou soluções.")
        validate_instrument_reagent_compatibility(instrument, reagent)

        if source_container_name is None:
            _ensure_container_meta(state, target_container_name)
            _add_content(state, target_container_name, reagent_id, amount_value, unit_value_str)
            _apply_reaction_if_matches(db, state, target_container_name)
            state.current_step_index += 1
            state.message = f"Passo concluído: {current_step.text_instruction}"
            return _state_to_dict(state)

        source_meta = _ensure_container_meta(state, source_container_name)
        target_meta = _ensure_container_meta(state, target_container_name)
        _ = source_meta, target_meta

        source_contents = state.containers.setdefault(source_container_name, [])
        _remove_content(source_contents, reagent_id, amount_value, unit_value_str)
        _add_content(state, target_container_name, reagent_id, amount_value, unit_value_str)
        _apply_reaction_if_matches(db, state, target_container_name)
        state.current_step_index += 1
        state.message = f"Passo concluído: {current_step.text_instruction}"
        return _state_to_dict(state)

    if action_type == "pour_liquid_between_containers":
        if source_container_name is None or target_container_name is None:
            raise BadRequestError("É necessário informar o recipiente de origem e destino para esta ação.")
        source_meta = _ensure_container_meta(state, source_container_name)
        target_meta = _ensure_container_meta(state, target_container_name)
        _ = source_meta, target_meta

        source_contents = state.containers.setdefault(source_container_name, [])
        target_contents = state.containers.setdefault(target_container_name, [])

        for item in list(source_contents):
            reagent = db.get(Reagent, item.reagent_id)
            if not reagent:
                raise NotFoundError("Reagente não encontrado.")
            if reagent.physical_state not in {"liquid", "solution"}:
                raise BadRequestError("Somente líquidos ou soluções podem ser despejados entre recipientes.")
            _add_content(state, target_container_name, item.reagent_id, item.amount_value, item.amount_unit)

        state.containers[source_container_name] = []
        _apply_reaction_if_matches(db, state, target_container_name)
        state.current_step_index += 1
        state.message = f"Passo concluído: {current_step.text_instruction}"
        return _state_to_dict(state)

    raise BadRequestError("Tipo de ação inválido ou não suportado.")
