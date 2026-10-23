from lab3.core.unknown_code_error import UnknownCodeError
from lab3.item.armor import Armor
from lab3.item.item import Item
from lab3.item.weapon import Weapon


class ItemCatalog:
    """Каталог хранит шаблоны предметов, а наружу отдаёт только их копии."""

    def __init__(self):
        self._prototypes: dict[str, Item] = {}

    def register(self, prototype: Item) -> None:
        self._prototypes[prototype.code] = prototype

    def create(self, code: str) -> Item:
        """Каталог не знает конкретный класс шаблона: копию создаёт сам шаблон."""
        prototype = self._prototypes.get(code)
        if prototype is None:
            raise UnknownCodeError("Предмет", code)
        return prototype.copy()

    def create_weapon(self, code: str) -> Weapon:
        item = self.create(code)
        if isinstance(item, Weapon):
            return item
        raise ValueError(f"Предмет '{code}' не является оружием")

    def create_armor(self, code: str) -> Armor:
        item = self.create(code)
        if isinstance(item, Armor):
            return item
        raise ValueError(f"Предмет '{code}' не является броней")

    def get_codes(self) -> list[str]:
        return list(self._prototypes)