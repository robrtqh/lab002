from enum import Enum

from lab3.core.unknown_code_error import UnknownCodeError
from lab3.defense.armor_handler import ArmorHandler
from lab3.defense.barrier_handler import BarrierHandler
from lab3.defense.damage_handler import DamageHandler
from lab3.defense.evasion_handler import EvasionHandler
from lab3.item.armor import Armor
from lab3.item.item_catalog import ItemCatalog
from lab3.kit.mage_kit_factory import MageKitFactory
from lab3.kit.ranger_kit_factory import RangerKitFactory
from lab3.kit.starter_kit_factory import StarterKitFactory
from lab3.kit.warrior_kit_factory import WarriorKitFactory


class HeroClass(Enum):
    # (код, имя, здоровье, фабрика снаряжения, уклонение, барьер)
    WARRIOR = ("warrior", "Воин", 120, WarriorKitFactory, 0, 0)
    RANGER = ("ranger", "Следопыт", 100, RangerKitFactory, 0.15, 0)
    MAGE = ("mage", "Маг", 85, MageKitFactory, 0, 30)

    def __init__(self, code, display_name, base_health, kit_factory, evasion, barrier):
        self.code = code
        self.display_name = display_name
        self.base_health = base_health
        self._kit_factory = kit_factory
        self.evasion = evasion
        self.barrier = barrier

    def get_starter_kit(self, catalog: ItemCatalog) -> StarterKitFactory:
        return self._kit_factory(catalog)

    def create_defense(self, armor: Armor, level: int) -> DamageHandler:
        """Собирает цепочку защиты: уклонение -> броня -> барьер (звенья без значения не создаются)."""
        evasion = self.evasion
        barrier = self.barrier
        if self is HeroClass.WARRIOR and level >= 3:
            barrier = 20
        elif self is HeroClass.RANGER and level >= 5:
            barrier = 15
        elif self is HeroClass.MAGE and level >= 3:
            evasion = 0.10

        armor_handler = ArmorHandler(armor.defense)
        first: DamageHandler = armor_handler
        if evasion > 0:
            first = EvasionHandler(evasion)
            first.set_next(armor_handler)
        if barrier > 0:
            armor_handler.set_next(BarrierHandler(barrier))
        return first

    @staticmethod
    def by_code(code: str) -> "HeroClass":
        for hero_class in HeroClass:
            if hero_class.code == code:
                return hero_class
        raise UnknownCodeError("Класс героя", code)