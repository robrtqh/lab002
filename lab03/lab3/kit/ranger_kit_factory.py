from lab3.item.armor import Armor
from lab3.item.default_catalog import DefaultCatalog
from lab3.item.item_catalog import ItemCatalog
from lab3.item.weapon import Weapon
from lab3.kit.starter_kit_factory import StarterKitFactory


class RangerKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog):
        self._catalog = catalog

    def create_weapon(self) -> Weapon:
        return self._catalog.create_weapon(DefaultCatalog.HUNTING_BOW)

    def create_armor(self) -> Armor:
        return self._catalog.create_armor(DefaultCatalog.LEATHER_ARMOR)