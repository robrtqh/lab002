from lab3.core.dice import Dice
from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler


class EvasionHandler(DamageHandler):
    def __init__(self, chance: float):
        super().__init__()
        self._chance = chance

    def handle(self, damage: Damage) -> None:
        if Dice.get_instance().chance(self._chance):
            damage.evade()
            return  # удар не прошёл, дальше по цепочке не передаём
        self._pass_to_next(damage)