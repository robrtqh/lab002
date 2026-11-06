from lab3.combat.hit import Hit
from lab3.core.dice import Dice
from lab3.defense.armor_handler import ArmorHandler
from lab3.enemy.abstract_enemy import AbstractEnemy

RESISTANCE = 0.25
FIRE_BREATH_CHANCE = 0.25
FIRE_BREATH_MULTIPLIER = 2


class Dragon(AbstractEnemy):
    """Чешуя работает как броня, иногда дракон дышит огнём."""

    def __init__(self):
        super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400, ArmorHandler(RESISTANCE))

    def roll_damage(self) -> Hit:
        bite = super().roll_damage()
        if Dice.get_instance().chance(FIRE_BREATH_CHANCE):
            return Hit(bite.damage * FIRE_BREATH_MULTIPLIER, True)
        return bite