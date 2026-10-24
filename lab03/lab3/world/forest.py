from lab3.enemy.enemy import Enemy
from lab3.enemy.goblin import Goblin
from lab3.item.default_catalog import DefaultCatalog
from lab3.item.item_catalog import ItemCatalog
from lab3.world.location import Location


class Forest(Location):
    CODE = "forest"

    def __init__(self, catalog: ItemCatalog):
        super().__init__(Forest.CODE, "Мистический лес", 1, catalog)

    def _create_enemy(self) -> Enemy:
        return Goblin()

    def _get_loot_table(self) -> list:
        return [DefaultCatalog.GOBLIN_CLEAVER, DefaultCatalog.HUNTING_BOW, DefaultCatalog.LEATHER_ARMOR]