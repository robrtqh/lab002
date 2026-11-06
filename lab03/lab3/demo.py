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

def demo_strategy():
    from lab3.hero.hero_class import HeroClass
    from lab3.item.default_catalog import DefaultCatalog
    from lab3.tactic.aggressive_tactic import AggressiveTactic
    from lab3.tactic.balanced_tactic import BalancedTactic
    from lab3.tactic.cautious_tactic import CautiousTactic
    from lab3.world.crypt import Crypt

    print("===== Стратегия =====")
    catalog = DefaultCatalog.create()
    crypt = Crypt(catalog)
    for tactic in (BalancedTactic(), AggressiveTactic(), CautiousTactic()):
        mage = new_hero("Мерлин", HeroClass.MAGE, 2, catalog)
        report = crypt.explore(mage, tactic, 9)
        print(
            f"{tactic.display_name}: {describe_outcome(report)}, раундов {count_rounds(report)}, "
            f"у героя осталось {mage.health}/{mage.max_health} здоровья"
        )

def demo_decorator():
    from lab3.core.dice import Dice
    from lab3.enemy.armored_enemy import ArmoredEnemy
    from lab3.enemy.dragon import Dragon
    from lab3.enemy.goblin import Goblin
    from lab3.enemy.legendary_enemy import LegendaryEnemy
    from lab3.enemy.windfury_enemy import WindfuryEnemy

    print("\n===== Декоратор =====")
    enemies = [
        Goblin(),
        LegendaryEnemy(Goblin()),
        WindfuryEnemy(Goblin()),
        LegendaryEnemy(WindfuryEnemy(Goblin())),
        ArmoredEnemy(Goblin()),
        ArmoredEnemy(LegendaryEnemy(WindfuryEnemy(Dragon()))),
    ]
    for enemy in enemies:
        Dice.get_instance().reseed(5)
        hits = [str(enemy.roll_damage().damage) for _ in range(3)]
        received = enemy.receive_hit(20)
        print(
            f"{enemy.name}: удары {', '.join(hits)}, награда {enemy.experience_reward} опыта; "
            f"входящий урон 20 -> {received.amount}, здоровье {enemy.health}/{enemy.max_health}"
        )

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    demo_chain()
    demo_strategy() 
    demo_decorator()


if __name__ == "__main__":
    main()