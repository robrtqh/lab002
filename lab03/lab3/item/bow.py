from lab3.combat.hit import Hit
from lab3.core.dice import Dice
from lab3.item.weapon import Weapon

CRITICAL_MULTIPLIER = 2


class Bow(Weapon):
    """Лук с некоторым шансом наносит критический двойной урон."""

    def __init__(self, code, name, base_price, damage, critical_chance, enchantments=()):
        super().__init__(code, name, base_price, damage, enchantments)
        self._critical_chance = critical_chance

    def roll_damage(self) -> Hit:
        if Dice.get_instance().chance(self._critical_chance):
            return Hit(self.damage * CRITICAL_MULTIPLIER, True)
        return Hit(self.damage, False)

    def copy(self) -> "Bow":
        return Bow(
            self._code, self._name, self._base_price, self._damage,
            self._critical_chance, self._enchantments,
        )

    @property
    def description(self) -> str:
        return f"урон {self.damage}, шанс крита {round(self._critical_chance * 100)}%"