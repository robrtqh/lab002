from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler


class BarrierHandler(DamageHandler):
    def __init__(self, strength: int):
        super().__init__()
        self._strength = strength

    def handle(self, damage: Damage) -> None:
        absorbed = min(self._strength, damage.amount)
        if absorbed > 0:
            self._strength -= absorbed
            damage.absorb(absorbed)
        self._pass_to_next(damage)