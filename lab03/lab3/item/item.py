from abc import ABC, abstractmethod

from lab3.item.enchantment import Enchantment


class Item(ABC):
    def __init__(self, code: str, name: str, base_price: int, enchantments=()):
        self._code = code
        self._name = name
        self._base_price = base_price
        # ВАЖНО: всегда создаём новый список, иначе копия и оригинал
        # будут делить один список зачарований (поверхностное копирование)
        self._enchantments: list[Enchantment] = list(enchantments)

    @abstractmethod
    def copy(self) -> "Item":
        """Каждый наследник сам создаёт свою копию (паттерн Прототип)."""

    @property
    @abstractmethod
    def possible_enchantments(self) -> tuple[Enchantment, ...]:
        """Какие зачарования подходят этому предмету."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Описание характеристик, например 'урон 12'."""

    def enchant(self, enchantment: Enchantment) -> None:
        if enchantment not in self.possible_enchantments:
            raise ValueError(
                f"Зачарование '{enchantment.name}' не подходит для предмета '{self._name}'"
            )
        self._enchantments.append(enchantment)

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> int:
        return self._base_price + sum(e.bonus_price for e in self._enchantments)

    @property
    def enchantments(self) -> tuple[Enchantment, ...]:
        return tuple(self._enchantments)