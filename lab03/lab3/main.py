import sys
from pathlib import Path

from lab3.combat.outcome import Outcome
from lab3.console_view import ConsoleView
from lab3.game.game_facade import GameFacade

SAVE_FILE = Path("saves") / "heroes.json"
VIEW = ConsoleView()


def read_choice(count: int) -> int:
    """Читает номер варианта от 1 до count, возвращает индекс или -1."""
    try:
        choice = int(input().strip())
    except ValueError:
        return -1
    return choice - 1 if 1 <= choice <= count else -1


def choose_hero(game: GameFacade) -> str:
    saved = game.get_heroes()
    if saved:
        print("Выберите героя (0 - создать нового):")
        for i, hero in enumerate(saved, start=1):
            print(f"{i} - {hero.name}, {hero.hero_class.display_name} {hero.level} ур.")
        index = read_choice(len(saved))
        if index >= 0:
            name = saved[index].name
            print(f"{name} возвращается в лагерь на опушке мистического леса.")
            return name

    name = create_hero(game)
    print(f"{name} разбивает лагерь на опушке мистического леса.")
    return name


def create_hero(game: GameFacade) -> str:
    print("Создайте своего героя!")
    while True:
        print("Выберите класс:")
        hero_classes = game.get_hero_classes()
        for i, hero_class in enumerate(hero_classes, start=1):
            weapon, armor = game.get_starter_kit(hero_class.code)
            print(
                f"{i} - {hero_class.display_name} (здоровье {hero_class.base_health}, "
                f"{VIEW.describe_class(hero_class)}): {VIEW.describe(weapon)}, {VIEW.describe(armor)}"
            )
        index = read_choice(len(hero_classes))
        if index < 0:
            continue

        print("Введите имя:")
        name = input().strip()
        try:
            return game.create_hero(name, hero_classes[index].code).name
        except ValueError as e:
            print("Не получилось создать героя:", e)


def go_on_expedition(game: GameFacade, hero_name: str) -> None:
    locations = game.get_locations()
    print("Куда отправимся?")
    for i, location in enumerate(locations, start=1):
        print(f"{i} - {location.display_name} (рекомендуемый уровень {location.recommended_level})")
    location_index = read_choice(len(locations))
    if location_index < 0:
        return

    tactics = game.get_tactics()
    print("Какой тактики держаться в бою?")
    for i, tactic in enumerate(tactics, start=1):
        print(f"{i} - {tactic.display_name}: {tactic.description}")
    tactic_index = read_choice(len(tactics))
    if tactic_index < 0:
        return

    location = locations[location_index]
    report = game.explore(hero_name, location.code, tactics[tactic_index].code)
    print()
    VIEW.print_report(report, location.display_name)

    if report.battle.outcome == Outcome.VICTORY and report.battle.enemy.code == "dragon":
        print(f"\nДракон повержен! Барды еще долго будут петь о подвиге героя по имени {hero_name}.")


def manage_equipment(game: GameFacade, hero_name: str) -> None:
    inventory = game.get_hero(hero_name).inventory
    if not inventory:
        print("Инвентарь пуст")
        return
    print("Что экипировать? (0 - назад)")
    for i, item in enumerate(inventory, start=1):
        print(f"{i} - {VIEW.describe(item)}")
    index = read_choice(len(inventory))
    if index < 0:
        return
    item = game.equip(hero_name, index)
    print("Экипировано: " + VIEW.describe(item))


def visit_merchant(game: GameFacade, hero_name: str) -> None:
    print(f'Торговец: "Чего желаешь?" (золото: {game.get_hero(hero_name).gold})')
    print("1 - купить, 2 - продать, 0 - назад")
    answer = input().strip()
    if answer == "1":
        buy(game, hero_name)
    elif answer == "2":
        sell(game, hero_name)


def buy(game: GameFacade, hero_name: str) -> None:
    showcase = game.get_showcase()
    for i, item in enumerate(showcase, start=1):
        print(f"{i} - {VIEW.describe(item)}: {item.price} золота")
    index = read_choice(len(showcase))
    if index < 0:
        return
    try:
        item = game.buy(hero_name, showcase[index].code)
        print("Куплено: " + VIEW.describe(item))
    except RuntimeError as e:
        print(e)


def sell(game: GameFacade, hero_name: str) -> None:
    inventory = game.get_hero(hero_name).inventory
    if not inventory:
        print("Продавать нечего (экипированные предметы продать нельзя)")
        return
    for i, item in enumerate(inventory, start=1):
        print(f"{i} - {VIEW.describe(item)}: {game.get_sell_price(item)} золота")
    index = read_choice(len(inventory))
    if index < 0:
        return
    item_name = inventory[index].name
    price = game.sell(hero_name, index)
    print(f"Продано: {item_name} за {price} золота")


def print_journal(game: GameFacade, hero_name: str) -> None:
    journal = game.get_journal(hero_name)
    if not journal:
        print("В этот раз экспедиций еще не было")
        return
    for i, report in enumerate(journal, start=1):
        print(f"{i}. " + VIEW.summarize(
            report,
            game.get_location(report.location_code).display_name,
            game.get_tactic(report.tactic_code).display_name,
        ))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print("Файл сохранения:", SAVE_FILE.resolve())
    game = GameFacade(SAVE_FILE)
    hero_name = choose_hero(game)

    while True:
        print()
        VIEW.print_hero(game.get_hero(hero_name))
        print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, "
              "4 - журнал экспедиций, 0 - выйти из игры")
        answer = input().strip()
        if answer == "1":
            go_on_expedition(game, hero_name)
        elif answer == "2":
            manage_equipment(game, hero_name)
        elif answer == "3":
            visit_merchant(game, hero_name)
        elif answer == "4":
            print_journal(game, hero_name)
        elif answer == "0":
            return
        else:
            print("Такого варианта нет")


if __name__ == "__main__":
    main()