from __future__ import annotations

from dataclasses import dataclass

from lab3.combat.combatant import Combatant


@dataclass(frozen=True)
class Participant:
    """Участник боя в том виде, в котором он попадает в отчёт."""
    code: str
    name: str
    max_health: int

    @staticmethod
    def of(combatant: Combatant) -> Participant:
        return Participant(combatant.code, combatant.name, combatant.max_health)