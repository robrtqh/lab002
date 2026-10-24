from lab3.combat.hit import Hit
from lab3.core.dice import Dice
from lab3.core.mathutil import round_half_up
from lab3.enemy.abstract_enemy import AbstractEnemy

RESISTANCE = 0.25
FIRE_BREATH_CHANCE = 0.25
FIRE_BREATH_MULTIPLIER = 2


class Dragon(AbstractEnemy):
    """Дракон защищён чешуёй и время от времени дышит огнём."""

    def __init__(self):
        super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400)

    def roll_damage(self) -> Hit:
        bite = super().roll_damage()
        if Dice.get_instance().chance(FIRE_BREATH_CHANCE):
            return Hit(bite.damage * FIRE_BREATH_MULTIPLIER, True)
        return bite

    def _reduce_damage(self, damage: int) -> int:
        return round_half_up(damage * (1 - RESISTANCE))