from lab3.enemy.dragon import Dragon
from lab3.enemy.enemy import Enemy
from lab3.item.default_catalog import DefaultCatalog
from lab3.item.item_catalog import ItemCatalog
from lab3.world.location import Location


class DragonLair(Location):
    CODE = "dragon-lair"

    def __init__(self, catalog: ItemCatalog):
        super().__init__(DragonLair.CODE, "Логово дракона", 5, catalog)

    def _create_enemy(self) -> Enemy:
        return Dragon()

    def _get_loot_table(self) -> list:
        return [DefaultCatalog.DAWN_BLADE, DefaultCatalog.DRAGONSCALE_ARMOR]