from dataclasses import dataclass
from typing import Any

from lab3.event.game_event_type import GameEventType


@dataclass(frozen=True)
class GameEvent:
    """Просто данные: что произошло, с каким героем и в какой экспедиции."""
    type: GameEventType
    hero: Any
    expedition: Any