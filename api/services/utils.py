from __future__ import annotations

from core.exceptions import BadRequestError
from models.instrument import Instrument
from models.reagent import Reagent


def validate_instrument_reagent_compatibility(
    instrument: Instrument,
    reagent: Reagent,
) -> None:
    allowed_states_raw = (instrument.allowed_physical_states or "").strip()
    if not allowed_states_raw:
        return

    allowed_states = {state.strip() for state in allowed_states_raw.split(",") if state.strip()}
    if not allowed_states:
        return

    if reagent.physical_state not in allowed_states:
        raise BadRequestError(
            "Este instrumento não é compatível com o estado físico do reagente."
        )
