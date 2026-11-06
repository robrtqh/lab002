import sys

from lab3.console_view import ConsoleView

VIEW = ConsoleView()


def new_hero(name, hero_class, level, catalog):
    from lab3.hero.hero import Hero
    return (
        Hero.Builder().set_name(name).set_hero_class(hero_class)
        .set_starter_kit(hero_class.get_starter_kit(catalog)).set_level(level).build()
    )


def describe_outcome(report) -> str:
    return "победа" if report.battle.outcome.name == "VICTORY" else "поражение"


def count_rounds(report) -> int:
    return report.battle.events[-1].round


def print_hits(title, chain, count):
    from lab3.defense.damage import Damage
    results = []
    for _ in range(count):
        damage = Damage(30)
        chain.handle(damage)
        if damage.evaded:
            results.append("уклонение")
        elif damage.absorbed > 0:
            results.append(f"поглощено {damage.absorbed}, прошло {damage.amount}")
        else:
            results.append(f"прошло {damage.amount}")
    print(f"{title}: {'; '.join(results)}")


def demo_chain():
    from lab3.core.dice import Dice
    from lab3.defense.armor_handler import ArmorHandler
    from lab3.defense.barrier_handler import BarrierHandler
    from lab3.defense.evasion_handler import EvasionHandler

    print("===== Цепочка обязанностей =====")
    print_hits("Броня 30%", ArmorHandler(0.3), 2)

    armor_and_barrier = ArmorHandler(0.3)
    armor_and_barrier.set_next(BarrierHandler(30))
    print_hits("Броня 30% -> барьер 30", armor_and_barrier, 3)

    Dice.get_instance().reseed(3)
    full_chain = EvasionHandler(0.5)
    full_chain.set_next(ArmorHandler(0.3)).set_next(BarrierHandler(30))
    print_hits("Уклонение 50% -> броня 30% -> барьер 30", full_chain, 3)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    demo_chain()


if __name__ == "__main__":
    main()