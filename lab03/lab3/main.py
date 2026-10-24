import sys

from lab3.camp.merchant import Merchant
from lab3.combat.outcome import Outcome
from lab3.console_view import ConsoleView
from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item.default_catalog import DefaultCatalog
from lab3.world.crypt import Crypt
from lab3.world.dragon_lair import DragonLair
from lab3.world.forest import Forest
from lab3.world.location_registry import LocationRegistry

VIEW = ConsoleView()


def read_choice(count: int) -> int:
    """Читает номер варианта от 1 до count, возвращает индекс или -1, если ввели что-то другое."""
    try:
        choice = int(input().strip())
    except ValueError:
        return -1
    return choice - 1 if 1 <= choice <= count else -1


def create_hero(catalog) -> Hero:
    print("Создайте своего героя!")
    while True:
        print("Выберите класс:")
        hero_classes = list(HeroClass)
        for i, hero_class in enumerate(hero_classes, start=1):
            kit = hero_class.get_starter_kit(catalog)
            print(
                f"{i} - {hero_class.display_name} (здоровье {hero_class.base_health}): "
                f"{VIEW.describe(kit.create_weapon())}, {VIEW.describe(kit.create_armor())}"
            )
        index = read_choice(len(hero_classes))
        if index < 0:
            continue
        hero_class = hero_classes[index]

        print("Введите имя:")
        name = input().strip()
        try:
            return (
                Hero.Builder()
                .set_name(name)
                .set_hero_class(hero_class)
                .set_starter_kit(hero_class.get_starter_kit(catalog))
                .build()
            )
        except ValueError as e:
            print("Не получилось создать героя:", e)


def go_on_expedition(hero, locations) -> None:
    all_locations = locations.get_all()
    print("Куда отправимся?")
    for i, location in enumerate(all_locations, start=1):
        print(f"{i} - {location.display_name} (рекомендуемый уровень {location.recommended_level})")
    index = read_choice(len(all_locations))
    if index < 0:
        return

    location = all_locations[index]
    report = location.explore(hero)
    print()
    VIEW.print_report(report, location.display_name)

    if report.battle.outcome == Outcome.VICTORY and location.code == DragonLair.CODE:
        print(f"\nДракон повержен! Барды еще долго будут петь о подвиге героя по имени {hero.name}.")


def manage_equipment(hero) -> None:
    inventory = hero.inventory
    if not inventory:
        print("Инвентарь пуст")
        return
    print("Что экипировать? (0 - назад)")
    for i, item in enumerate(inventory, start=1):
        print(f"{i} - {VIEW.describe(item)}")
    index = read_choice(len(inventory))
    if index < 0:
        return
    hero.equip(inventory[index])
    print("Экипировано: " + VIEW.describe(inventory[index]))


def visit_merchant(hero, merchant) -> None:
    print(f'Торговец: "Чего желаешь?" (золото: {hero.gold})')
    print("1 - купить, 2 - продать, 0 - назад")
    answer = input().strip()
    if answer == "1":
        buy(hero, merchant)
    elif answer == "2":
        sell(hero, merchant)


def buy(hero, merchant) -> None:
    showcase = merchant.get_showcase()
    for i, item in enumerate(showcase, start=1):
        print(f"{i} - {VIEW.describe(item)}: {item.price} золота")
    index = read_choice(len(showcase))
    if index < 0:
        return
    try:
        item = merchant.buy(hero, showcase[index].code)
        print("Куплено: " + VIEW.describe(item))
    except RuntimeError as e:
        print(e)


def sell(hero, merchant) -> None:
    inventory = hero.inventory
    if not inventory:
        print("Продавать нечего (экипированные предметы продать нельзя)")
        return
    for i, item in enumerate(inventory, start=1):
        print(f"{i} - {VIEW.describe(item)}: {merchant.get_sell_price(item)} золота")
    index = read_choice(len(inventory))
    if index < 0:
        return
    item = inventory[index]
    price = merchant.sell(hero, item)
    print(f"Продано: {item.name} за {price} золота")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # чтобы кириллица не ломалась в Windows

    catalog = DefaultCatalog.create()
    locations = LocationRegistry([Forest(catalog), Crypt(catalog), DragonLair(catalog)])
    merchant = Merchant(catalog, [
        DefaultCatalog.IRON_SWORD, DefaultCatalog.ELVEN_BOW, DefaultCatalog.EMBER_STAFF,
        DefaultCatalog.CHAINMAIL, DefaultCatalog.PLATE_ARMOR,
    ])

    hero = create_hero(catalog)
    print(f"{hero.name} разбивает лагерь на опушке мистического леса.")

    while True:
        print()
        VIEW.print_hero(hero)
        print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, 0 - выйти из игры")
        answer = input().strip()
        if answer == "1":
            go_on_expedition(hero, locations)
        elif answer == "2":
            manage_equipment(hero)
        elif answer == "3":
            visit_merchant(hero, merchant)
        elif answer == "0":
            return
        else:
            print("Такого варианта нет")


if __name__ == "__main__":
    main()