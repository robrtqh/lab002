from dataclasses import dataclass

from lab3.combat.event_type import EventType
from lab3.combat.side import Side


@dataclass(frozen=True)
class BattleEvent:
    round: int
    type: EventType
    source: Side
    target: Side
    amount: int
    target_health_after: int