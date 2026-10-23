from lab3.item.armor import Armor
from lab3.item.bow import Bow
from lab3.item.item_catalog import ItemCatalog
from lab3.item.staff import Staff
from lab3.item.sword import Sword


class DefaultCatalog:
    """Все предметы, которые есть в игре."""

    # стартовое снаряжение
    TRAINING_SWORD = "training-sword"
    HUNTING_BOW = "hunting-bow"
    APPRENTICE_STAFF = "apprentice-staff"
    CHAINMAIL = "chainmail"
    LEATHER_ARMOR = "leather-armor"
    LINEN_ROBE = "linen-robe"

    # товары торговца
    IRON_SWORD = "iron-sword"
    ELVEN_BOW = "elven-bow"
    EMBER_STAFF = "ember-staff"
    PLATE_ARMOR = "plate-armor"

    # добыча
    GOBLIN_CLEAVER = "goblin-cleaver"
    BONE_BOW = "bone-bow"
    NECROMANCER_STAFF = "necromancer-staff"
    KNIGHT_BLADE = "knight-blade"
    CRYPT_MAIL = "crypt-mail"
    DAWN_BLADE = "dawn-blade"
    DRAGONSCALE_ARMOR = "dragonscale-armor"

    @staticmethod
    def create() -> ItemCatalog:
        c = DefaultCatalog
        catalog = ItemCatalog()

        # стартовое снаряжение
        catalog.register(Sword(c.TRAINING_SWORD, "Тренировочный меч", 20, 12))
        catalog.register(Bow(c.HUNTING_BOW, "Охотничий лук", 20, 10, 0.3))
        catalog.register(Staff(c.APPRENTICE_STAFF, "Посох ученика", 20, 14, 0.3))
        catalog.register(Armor(c.CHAINMAIL, "Кольчуга", 40, 0.3))
        catalog.register(Armor(c.LEATHER_ARMOR, "Кожаная броня", 30, 0.2))
        catalog.register(Armor(c.LINEN_ROBE, "Льняная роба", 15, 0.1))

        # товары торговца
        catalog.register(Sword(c.IRON_SWORD, "Железный меч", 80, 17))
        catalog.register(Bow(c.ELVEN_BOW, "Эльфийский лук", 90, 14, 0.4))
        catalog.register(Staff(c.EMBER_STAFF, "Тлеющий посох", 90, 20, 0.3))
        catalog.register(Armor(c.PLATE_ARMOR, "Латы", 120, 0.4))

        # добыча
        catalog.register(Sword(c.GOBLIN_CLEAVER, "Гоблинский тесак", 40, 15))
        catalog.register(Bow(c.BONE_BOW, "Костяной лук", 140, 17, 0.4))
        catalog.register(Staff(c.NECROMANCER_STAFF, "Посох некроманта", 150, 25, 0.35))
        catalog.register(Sword(c.KNIGHT_BLADE, "Клинок рыцаря", 150, 23))
        catalog.register(Armor(c.CRYPT_MAIL, "Кольчуга стража склепа", 160, 0.45))
        catalog.register(Sword(c.DAWN_BLADE, "Клинок рассвета", 500, 35))
        catalog.register(Armor(c.DRAGONSCALE_ARMOR, "Драконья чешуя", 500, 0.55))

        return catalog