from abc import abstractmethod

from lab3.combat.hit import Hit
from lab3.item import enchantment as enchantments
from lab3.item.item import Item


class Weapon(Item):
    def __init__(self, code: str, name: str, base_price: int, damage: int, enchantments=()):
        super().__init__(code, name, base_price, enchantments)
        self._damage = damage

    @abstractmethod
    def roll_damage(self) -> Hit:
        """Как именно оружие наносит урон, решают наследники."""

    @abstractmethod
    def copy(self) -> "Weapon": ...

    @property
    def damage(self) -> int:
        """Урон с учётом зачарований."""
        return self._damage + sum(e.bonus_damage for e in self._enchantments)

    @property
    def possible_enchantments(self):
        return enchantments.FOR_WEAPONS