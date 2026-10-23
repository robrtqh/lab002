from enum import Enum

from lab3.core.unknown_code_error import UnknownCodeError
from lab3.item.item_catalog import ItemCatalog
from lab3.kit.mage_kit_factory import MageKitFactory
from lab3.kit.ranger_kit_factory import RangerKitFactory
from lab3.kit.starter_kit_factory import StarterKitFactory
from lab3.kit.warrior_kit_factory import WarriorKitFactory


class HeroClass(Enum):
    # (код, отображаемое имя, базовое здоровье, класс фабрики стартового набора)
    WARRIOR = ("warrior", "Воин", 120, WarriorKitFactory)
    RANGER = ("ranger", "Следопыт", 100, RangerKitFactory)
    MAGE = ("mage", "Маг", 85, MageKitFactory)

    def __init__(self, code, display_name, base_health, kit_factory):
        self.code = code
        self.display_name = display_name
        self.base_health = base_health
        self._kit_factory = kit_factory

    def get_starter_kit(self, catalog: ItemCatalog) -> StarterKitFactory:
        """Каждый класс сам знает свою фабрику стартового снаряжения."""
        return self._kit_factory(catalog)

    @staticmethod
    def by_code(code: str) -> "HeroClass":
        for hero_class in HeroClass:
            if hero_class.code == code:
                return hero_class
        raise UnknownCodeError("Класс героя", code)