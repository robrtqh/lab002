from lab3.core.mathutil import round_half_up
from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler


class ArmorHandler(DamageHandler):
    def __init__(self, defense: float):
        super().__init__()
        self._defense = defense

    def handle(self, damage: Damage) -> None:
        reduced = round_half_up(damage.amount * (1 - self._defense))
        damage.reduce_to(max(1, reduced))
        self._pass_to_next(damage)