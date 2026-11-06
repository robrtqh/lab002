from lab3.core.dice import Dice
from lab3.enemy.enemy import Enemy
from lab3.enemy.haunted_weapon import HauntedWeapon
from lab3.item.default_catalog import DefaultCatalog
from lab3.item.item_catalog import ItemCatalog
from lab3.world.location import Location

HAUNTED_WEAPONS = [DefaultCatalog.IRON_SWORD, DefaultCatalog.ELVEN_BOW, DefaultCatalog.EMBER_STAFF]


class HauntedManor(Location):
    CODE = "haunted-manor"

    def __init__(self, catalog: ItemCatalog):
        super().__init__(HauntedManor.CODE, "Проклятый особняк", 2, catalog)

    def _create_enemy(self) -> Enemy:
        # фабричный метод: берём случайное оружие и оборачиваем в адаптер
        weapon = self._catalog.create_weapon(Dice.get_instance().pick(HAUNTED_WEAPONS))
        return HauntedWeapon(weapon)

    def _get_loot_table(self) -> list:
        return [
            DefaultCatalog.IRON_SWORD, DefaultCatalog.ELVEN_BOW,
            DefaultCatalog.EMBER_STAFF, DefaultCatalog.PLATE_ARMOR,
        ]