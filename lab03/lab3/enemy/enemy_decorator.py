from lab3.combat.hit import Hit
from lab3.defense.damage import Damage
from lab3.enemy.enemy import Enemy


class EnemyDecorator(Enemy):
    """Базовый декоратор: ничего не меняет, всё делегирует обёрнутому врагу."""

    def __init__(self, wrapped: Enemy):
        self._wrapped = wrapped

    @property
    def code(self) -> str:
        return self._wrapped.code

    @property
    def name(self) -> str:
        return self._wrapped.name

    @property
    def health(self) -> int:
        return self._wrapped.health

    @property
    def max_health(self) -> int:
        return self._wrapped.max_health

    @property
    def experience_reward(self) -> int:
        return self._wrapped.experience_reward

    def is_alive(self) -> bool:
        return self._wrapped.is_alive()

    def roll_damage(self) -> Hit:
        return self._wrapped.roll_damage()

    def receive_hit(self, damage: int) -> Damage:
        return self._wrapped.receive_hit(damage)

    def roll_gold_reward(self) -> int:
        return self._wrapped.roll_gold_reward()