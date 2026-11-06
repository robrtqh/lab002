from lab3.defense.armor_handler import ArmorHandler
from lab3.enemy.abstract_enemy import AbstractEnemy

RESISTANCE = 0.3


class Skeleton(AbstractEnemy):
    """Скелет: кости работают как броня."""

    def __init__(self):
        super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70, ArmorHandler(RESISTANCE))