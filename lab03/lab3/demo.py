import sys

from lab3.console_view import ConsoleView
from lab3.core.dice import Dice
from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item import enchantment
from lab3.item.default_catalog import DefaultCatalog
from lab3.world.crypt import Crypt
from lab3.world.forest import Forest


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    catalog = DefaultCatalog.create()
    view = ConsoleView()

    print("===== Одиночка =====")
    first = Dice.get_instance()
    second = Dice()
    print("Dice() и Dice.get_instance() - один и тот же объект:", first is second)

    print()
    print("===== Прототип =====")
    plain_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword.enchant(enchantment.FIERY)
    print("Первая копия:        " + view.describe(plain_sword))
    print("Вторая копия:        " + view.describe(fiery_sword))
    print("Новая копия шаблона: " + view.describe(catalog.create(DefaultCatalog.IRON_SWORD)))
    print("Копии - разные объекты:", plain_sword is not fiery_sword)

    print()
    print("===== Абстрактная фабрика =====")
    for hero_class in HeroClass:
        kit = hero_class.get_starter_kit(catalog)
        print(
            f"{hero_class.display_name}: {view.describe(kit.create_weapon())}, "
            f"{view.describe(kit.create_armor())}"
        )

    print()
    print("===== Строитель =====")
    hero = (
        Hero.Builder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
        .set_level(3)
        .build()
    )
    view.print_hero(hero)
    try:
        Hero.Builder().set_hero_class(HeroClass.MAGE) \
            .set_starter_kit(HeroClass.MAGE.get_starter_kit(catalog)).build()
    except ValueError as e:
        print("Герой без имени не создается:", e)
    try:
        Hero.Builder().set_name("Мерлин").build()
    except ValueError as e:
        print("Герой без класса не создается:", e)

    print()
    print("===== Фабричный метод =====")
    forest = Forest(catalog)
    crypt = Crypt(catalog)
    view.print_report(forest.explore(hero, 7), forest.display_name)
    print()
    view.print_report(crypt.explore(hero, 7), crypt.display_name)


if __name__ == "__main__":
    main()