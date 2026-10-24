from dataclasses import dataclass
from typing import Optional

from lab3.item.item import Item


@dataclass(frozen=True)
class Rewards:
    """Итоги экспедиции для героя. gold отрицательный при поражении, loot = None, если добычи нет."""
    experience: int
    gold: int
    loot: Optional[Item]
    levels_gained: int