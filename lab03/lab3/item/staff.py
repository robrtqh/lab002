from lab3.combat.hit import Hit
from lab3.core.dice import Dice
from lab3.item.weapon import Weapon


class Staff(Weapon):
    """Урон посоха непредсказуем: может быть больше или меньше базового."""

    def __init__(self, code, name, base_price, damage, scatter, enchantments=()):
        super().__init__(code, name, base_price, damage, enchantments)
        self._scatter = scatter

    def roll_damage(self) -> Hit:
        return Hit(Dice.get_instance().roll(self._min_damage(), self._max_damage()), False)

    def copy(self) -> "Staff":
        return Staff(
            self._code, self._name, self._base_price, self._damage,
            self._scatter, self._enchantments,
        )

    @property
    def description(self) -> str:
        return f"урон {self._min_damage()}-{self._max_damage()}"

    def _min_damage(self) -> int:
        return int(self.damage * (1 - self._scatter) + 0.5)

    def _max_damage(self) -> int:
        return int(self.damage * (1 + self._scatter) + 0.5)