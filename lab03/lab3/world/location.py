from abc import ABC, abstractmethod
from typing import Optional

from lab3.combat.battle import Battle
from lab3.combat.outcome import Outcome
from lab3.core.dice import Dice
from lab3.enemy.enemy import Enemy
from lab3.hero.hero import Hero
from lab3.item.item import Item
from lab3.item.item_catalog import ItemCatalog
from lab3.world.expedition_report import ExpeditionReport
from lab3.world.rewards import Rewards

LOOT_CHANCE = 0.6
ENCHANT_CHANCE = 0.3


class Location(ABC):
    def __init__(self, code: str, display_name: str, recommended_level: int, catalog: ItemCatalog):
        self._code = code
        self._display_name = display_name
        self._recommended_level = recommended_level
        self._catalog = catalog

    @abstractmethod
    def _create_enemy(self) -> Enemy:
        """ФАБРИЧНЫЙ МЕТОД: какого врага создать, решают подклассы."""

    @abstractmethod
    def _get_loot_table(self) -> list:
        """Коды предметов из каталога, которые можно найти в локации."""

    def explore(self, hero: Hero, seed: Optional[int] = None) -> ExpeditionReport:
        """Общая логика для всех локаций: враг, бой, награда."""
        dice = Dice.get_instance()
        if seed is None:
            seed = dice.next_seed()
        dice.reseed(seed)

        hero.restore_health()
        enemy = self._create_enemy()  # вызов фабричного метода
        battle = Battle(hero, enemy).run()

        if battle.outcome == Outcome.VICTORY:
            rewards = self._reward(hero, enemy, dice)
        else:
            rewards = self._punish(hero)
        return ExpeditionReport(seed, self._code, battle, rewards)

    def _reward(self, hero: Hero, enemy: Enemy, dice: Dice) -> Rewards:
        experience = enemy.experience_reward
        gold = enemy.roll_gold_reward()
        loot = self._roll_loot(dice)

        levels_gained = hero.gain_experience(experience)
        hero.add_gold(gold)
        if loot is not None:
            hero.add_item(loot)
        return Rewards(experience, gold, loot, levels_gained)

    def _roll_loot(self, dice: Dice) -> Optional[Item]:
        if not dice.chance(LOOT_CHANCE):
            return None
        # добыча - копия шаблона из каталога (прототип), зачаровываем именно копию
        loot = self._catalog.create(dice.pick(self._get_loot_table()))
        if dice.chance(ENCHANT_CHANCE):
            loot.enchant(dice.pick(list(loot.possible_enchantments)))
        return loot

    def _punish(self, hero: Hero) -> Rewards:
        """Проигравший герой теряет половину золота."""
        lost_gold = hero.gold // 2
        hero.spend_gold(lost_gold)
        return Rewards(0, -lost_gold, None, 0)

    @property
    def code(self) -> str:
        return self._code

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def recommended_level(self) -> int:
        return self._recommended_level