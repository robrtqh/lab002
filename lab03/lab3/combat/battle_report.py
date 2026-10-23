from dataclasses import dataclass

from lab3.combat.battle_event import BattleEvent
from lab3.combat.outcome import Outcome
from lab3.combat.participant import Participant


@dataclass(frozen=True)
class BattleReport:
    """Результат боя: кто сражался, чем закончилось и что происходило."""
    hero: Participant
    enemy: Participant
    outcome: Outcome
    events: tuple[BattleEvent, ...]