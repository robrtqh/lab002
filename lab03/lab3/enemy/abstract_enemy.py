from typing import Optional

from lab3.combat.hit import Hit
from lab3.core.dice import Dice
from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler
from lab3.enemy.enemy import Enemy


class AbstractEnemy(Enemy):
    """Общая логика врагов. Защита задаётся цепочкой обработчиков (или None)."""

    def __init__(self, code, name, max_health, min_damage, max_damage,
                 experience_reward, gold_reward, defense: Optional[DamageHandler] = None):
        self._code = code
        self._name = name
        self._max_health = max_health
        self._min_damage = min_damage
        self._max_damage = max_damage
        self._experience_reward = experience_reward
        self._gold_reward = gold_reward
        self._defense = defense
        self._health = max_health

    def roll_damage(self) -> Hit:
        return Hit(Dice.get_instance().roll(self._min_damage, self._max_damage), False)

    def receive_hit(self, amount: int) -> Damage:
        damage = Damage(amount)
        if self._defense is not None:
            self._defense.handle(damage)  # применение цепочки защиты
        self._health = max(0, self._health - damage.amount)
        return damage

    def is_alive(self) -> bool:
        return self._health > 0

    def roll_gold_reward(self) -> int:
        return Dice.get_instance().roll(self._gold_reward // 2, self._gold_reward)

    @property
    def experience_reward(self) -> int:
        return self._experience_reward

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._max_health