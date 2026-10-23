from lab3.combat.hit import Hit
from lab3.item.weapon import Weapon


class Sword(Weapon):
    """Урон меча всегда одинаковый."""

    def roll_damage(self) -> Hit:
        return Hit(self.damage, False)

    def copy(self) -> "Sword":
        return Sword(self._code, self._name, self._base_price, self._damage, self._enchantments)

    @property
    def description(self) -> str:
        return f"урон {self.damage}"