from abc import ABC, abstractmethod
from typing import Optional

from lab3.combat.battle import Battle
from lab3.combat.outcome import Outcome
from lab3.core.dice import Dice
from lab3.enemy.enemy import Enemy
from lab3.hero.hero import Hero
from lab3.item.item import Item
from lab3.item.item_catalog import ItemCatalog
from lab3.tactic.balanced_tactic import BalancedTactic
from lab3.tactic.tactic import Tactic
from lab3.world.expedition_report import ExpeditionReport
from lab3.world.rewards import Rewards

from lab3.enemy.armored_enemy import ArmoredEnemy
from lab3.enemy.legendary_enemy import LegendaryEnemy
from lab3.enemy.windfury_enemy import WindfuryEnemy

LOOT_CHANCE = 0.6
ENCHANT_CHANCE = 0.3
ELITE_CHANCE = 0.2
DOUBLE_ELITE_CHANCE = 0.25
ARMORED_CHANCE = 0.3


class Location(ABC):
    def __init__(self, code: str, display_name: str, recommended_level: int, catalog: ItemCatalog):
        self._code = code
        self._display_name = display_name
        self._recommended_level = recommended_level
        self._catalog = catalog

    @abstractmethod
    def _create_enemy(self) -> Enemy:
        """Фабричный метод: какого врага создать, решают подклассы."""

    @abstractmethod
    def _get_loot_table(self) -> list:
        """Коды предметов из каталога, которые можно найти в локации."""

    def explore(self, hero: Hero, tactic: Optional[Tactic] = None,
                seed: Optional[int] = None) -> ExpeditionReport:
        tactic = tactic or BalancedTactic()
        dice = Dice.get_instance()
        if seed is None:
            seed = dice.next_seed()
        dice.reseed(seed)

        hero.rest()
        enemy = self._create_enemy()
        if dice.chance(ELITE_CHANCE):
            enemy = self._make_elite(enemy, dice)  
        battle = Battle(hero, enemy, tactic).run()

        if battle.outcome == Outcome.VICTORY:
            rewards = self._reward(hero, enemy, dice)
        else:
            rewards = self._punish(hero)
        return ExpeditionReport(seed, self._code, tactic.code, battle, rewards)

    def _make_elite(self, enemy: Enemy, dice: Dice) -> Enemy:
        both = dice.chance(DOUBLE_ELITE_CHANCE)
        if dice.chance(0.5):
            enemy = LegendaryEnemy(enemy)
            if both:
                enemy = WindfuryEnemy(enemy)
        else:
            enemy = WindfuryEnemy(enemy)
            if both:
                enemy = LegendaryEnemy(enemy)
        return ArmoredEnemy(enemy) if dice.chance(ARMORED_CHANCE) else enemy
    
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
        loot = self._catalog.create(dice.pick(self._get_loot_table()))
        if dice.chance(ENCHANT_CHANCE):
            loot.enchant(dice.pick(list(loot.possible_enchantments)))
        return loot

    def _punish(self, hero: Hero) -> Rewards:
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