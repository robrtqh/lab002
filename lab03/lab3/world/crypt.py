from lab3.enemy.enemy import Enemy
from lab3.enemy.skeleton import Skeleton
from lab3.item.default_catalog import DefaultCatalog
from lab3.item.item_catalog import ItemCatalog
from lab3.world.location import Location


class Crypt(Location):
    CODE = "crypt"

    def __init__(self, catalog: ItemCatalog):
        super().__init__(Crypt.CODE, "Заброшенный склеп", 3, catalog)

    def _create_enemy(self) -> Enemy:
        return Skeleton()

    def _get_loot_table(self) -> list:
        return [
            DefaultCatalog.KNIGHT_BLADE, DefaultCatalog.BONE_BOW,
            DefaultCatalog.NECROMANCER_STAFF, DefaultCatalog.CRYPT_MAIL,
        ]