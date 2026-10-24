from lab3.core.mathutil import round_half_up
from lab3.enemy.abstract_enemy import AbstractEnemy

RESISTANCE = 0.3


class Skeleton(AbstractEnemy):
    """Скелет: кости плохо поддаются ударам, часть урона проходит мимо."""

    def __init__(self):
        super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70)

    def _reduce_damage(self, damage: int) -> int:
        return round_half_up(damage * (1 - RESISTANCE))