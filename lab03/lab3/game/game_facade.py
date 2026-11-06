from pathlib import Path

from lab3.camp.merchant import Merchant
from lab3.combat.outcome import Outcome
from lab3.core.unknown_code_error import UnknownCodeError
from lab3.event.game_event import GameEvent
from lab3.event.game_event_publisher import GameEventPublisher
from lab3.event.game_event_type import GameEventType
from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item.default_catalog import DefaultCatalog
from lab3.progress.achievement_tracker import AchievementTracker
from lab3.progress.expedition_journal import ExpeditionJournal
from lab3.storage.caching_hero_repository import CachingHeroRepository
from lab3.storage.file_hero_repository import FileHeroRepository
from lab3.tactic.aggressive_tactic import AggressiveTactic
from lab3.tactic.balanced_tactic import BalancedTactic
from lab3.tactic.cautious_tactic import CautiousTactic
from lab3.world.crypt import Crypt
from lab3.world.dragon_lair import DragonLair
from lab3.world.forest import Forest
from lab3.world.haunted_manor import HauntedManor
from lab3.world.location_registry import LocationRegistry


class GameFacade:
    """Фасад: прячет настройку и связи всех подсистем игры, логики в нём нет."""

    def __init__(self, save_file: Path):
        self._catalog = DefaultCatalog.create()
        self._locations = LocationRegistry([
            Forest(self._catalog), HauntedManor(self._catalog),
            Crypt(self._catalog), DragonLair(self._catalog),
        ])
        self._tactics = [BalancedTactic(), AggressiveTactic(), CautiousTactic()]
        self._merchant = Merchant(self._catalog, [
            DefaultCatalog.IRON_SWORD, DefaultCatalog.ELVEN_BOW, DefaultCatalog.EMBER_STAFF,
            DefaultCatalog.CHAINMAIL, DefaultCatalog.PLATE_ARMOR,
        ])
        # заместитель вместо настоящего хранилища
        self._heroes = CachingHeroRepository(FileHeroRepository(save_file, self._catalog))

        # связи издателя и подписчиков
        self._events = GameEventPublisher()
        self._journal = ExpeditionJournal()
        achievements = AchievementTracker()
        self._events.subscribe(GameEventType.VICTORY, achievements)
        self._events.subscribe(GameEventType.LEVEL_UP, achievements)
        self._events.subscribe(GameEventType.VICTORY, self._journal)
        self._events.subscribe(GameEventType.DEFEAT, self._journal)

    def get_hero_classes(self) -> list:
        return list(HeroClass)

    def get_starter_kit(self, hero_class_code: str) -> list:
        kit = HeroClass.by_code(hero_class_code).get_starter_kit(self._catalog)
        return [kit.create_weapon(), kit.create_armor()]

    def get_locations(self) -> list:
        return self._locations.get_all()

    def get_location(self, code: str):
        return self._locations.get(code)

    def get_tactics(self) -> list:
        return list(self._tactics)

    def get_tactic(self, code: str):
        for tactic in self._tactics:
            if tactic.code == code:
                return tactic
        raise UnknownCodeError("Тактика", code)

    def get_showcase(self) -> list:
        return self._merchant.get_showcase()

    def get_sell_price(self, item) -> int:
        return self._merchant.get_sell_price(item)

    def get_heroes(self) -> list:
        return self._heroes.find_all()

    def get_hero(self, name: str) -> Hero:
        hero = self._heroes.find_by_name(name)
        if hero is None:
            raise ValueError(f"Героя с именем {name} нет")
        return hero

    def create_hero(self, name: str, hero_class_code: str) -> Hero:
        if self._heroes.find_by_name(name) is not None:
            raise ValueError(f"Герой с именем {name} уже есть")
        hero_class = HeroClass.by_code(hero_class_code)
        hero = (
            Hero.Builder().set_name(name).set_hero_class(hero_class)
            .set_starter_kit(hero_class.get_starter_kit(self._catalog)).build()
        )
        self._heroes.save(hero)
        return hero

    def explore(self, hero_name: str, location_code: str, tactic_code: str):
        hero = self.get_hero(hero_name)
        report = self._locations.get(location_code).explore(hero, self.get_tactic(tactic_code))

        result = GameEventType.VICTORY if report.battle.outcome == Outcome.VICTORY else GameEventType.DEFEAT
        self._events.publish(GameEvent(result, hero, report))
        if report.rewards.levels_gained > 0:
            self._events.publish(GameEvent(GameEventType.LEVEL_UP, hero, report))

        self._heroes.save(hero)
        return report

    def equip(self, hero_name: str, inventory_index: int):
        hero = self.get_hero(hero_name)
        item = hero.inventory[inventory_index]
        hero.equip(item)
        self._heroes.save(hero)
        return item

    def buy(self, hero_name: str, item_code: str):
        hero = self.get_hero(hero_name)
        item = self._merchant.buy(hero, item_code)
        self._heroes.save(hero)
        return item

    def sell(self, hero_name: str, inventory_index: int) -> int:
        hero = self.get_hero(hero_name)
        price = self._merchant.sell(hero, hero.inventory[inventory_index])
        self._heroes.save(hero)
        return price

    def get_journal(self, hero_name: str) -> list:
        return self._journal.get_entries(hero_name)