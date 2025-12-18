from __future__ import annotations

from typing import Sequence

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.scenario import Scenario
from models.scenario_screen import ScenarioScreen
from models.scenario_screen_slider_image import ScenarioScreenSliderImage


def create_screens_for_scenario(
    db: Session,
    scenario: Scenario,
    screens_data: Sequence[dict],
    commit: bool = False,
) -> list[ScenarioScreen]:
    created: list[ScenarioScreen] = []
    for screen_data in sorted(
        screens_data,
        key=lambda s: s.get("order_index", 0) if isinstance(s, dict) else getattr(s, "order_index", 0),
    ):
        slider_images = screen_data.get("slider_images") if isinstance(screen_data, dict) else getattr(screen_data, "slider_images", None)
        screen = ScenarioScreen(
            scenario_id=scenario.id,
            order_index=screen_data["order_index"] if isinstance(screen_data, dict) else screen_data.order_index,
            screen_type=screen_data["screen_type"] if isinstance(screen_data, dict) else screen_data.screen_type,
            title=screen_data.get("title") if isinstance(screen_data, dict) else screen_data.title,
            body_text=screen_data.get("body_text") if isinstance(screen_data, dict) else screen_data.body_text,
            image_path=screen_data.get("image_path") if isinstance(screen_data, dict) else screen_data.image_path,
            gif_path=screen_data.get("gif_path") if isinstance(screen_data, dict) else screen_data.gif_path,
            button_label=screen_data.get("button_label") if isinstance(screen_data, dict) else screen_data.button_label,
            animation_key=screen_data.get("animation_key") if isinstance(screen_data, dict) else screen_data.animation_key,
        )
        db.add(screen)
        db.flush()

        if slider_images:
            for image_data in sorted(
                slider_images,
                key=lambda i: i.get("order_index", 0) if isinstance(i, dict) else getattr(i, "order_index", 0),
            ):
                screen.slider_images.append(
                    ScenarioScreenSliderImage(
                        screen_id=screen.id,
                        order_index=image_data["order_index"] if isinstance(image_data, dict) else image_data.order_index,
                        image_path=image_data["image_path"] if isinstance(image_data, dict) else image_data.image_path,
                        caption=image_data.get("caption") if isinstance(image_data, dict) else image_data.caption,
                    )
                )

        created.append(screen)

    if commit:
        db.commit()
        for screen in created:
            db.refresh(screen)

    return created


def list_screens_for_scenario(db: Session, scenario_id: int) -> list[ScenarioScreen]:
    return (
        db.query(ScenarioScreen)
        .filter(ScenarioScreen.scenario_id == scenario_id)
        .order_by(ScenarioScreen.order_index)
        .all()
    )


def get_screen(db: Session, screen_id: int) -> ScenarioScreen:
    screen = db.get(ScenarioScreen, screen_id)
    if not screen:
        raise NotFoundError("Tela de cenário não encontrada.")
    return screen
