from lab3.item import enchantment as enchantments
from lab3.item.item import Item

MAX_DEFENSE = 0.75  # больше этой доли урона никакая броня не поглощает


class Armor(Item):
    """Броня поглощает долю входящего урона."""

    def __init__(self, code, name, base_price, defense, enchantments=()):
        super().__init__(code, name, base_price, enchantments)
        self._defense = defense

    def copy(self) -> "Armor":
        return Armor(self._code, self._name, self._base_price, self._defense, self._enchantments)

    @property
    def defense(self) -> float:
        """Доля поглощаемого урона с учётом зачарований."""
        return min(self._defense + sum(e.bonus_defense for e in self._enchantments), MAX_DEFENSE)

    @property
    def possible_enchantments(self):
        return enchantments.FOR_ARMOR

    @property
    def description(self) -> str:
        return f"защита {round(self.defense * 100)}%"