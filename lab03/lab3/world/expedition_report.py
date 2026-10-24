from dataclasses import dataclass

from lab3.combat.battle_report import BattleReport
from lab3.world.rewards import Rewards


@dataclass(frozen=True)
class ExpeditionReport:
    seed: int
    location_code: str
    battle: BattleReport
    rewards: Rewards