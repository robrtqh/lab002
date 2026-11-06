from lab3.combat.hit import Hit
from lab3.enemy.enemy import Enemy
from lab3.enemy.enemy_decorator import EnemyDecorator

MULTIPLIER = 2


class LegendaryEnemy(EnemyDecorator):
    """Легендарный: двойной урон и двойная награда."""

    def __init__(self, wrapped: Enemy):
        super().__init__(wrapped)

    @property
    def name(self) -> str:
        return "Легендарный " + super().name

    def roll_damage(self) -> Hit:
        hit = super().roll_damage()  # super() = обёрнутый объект, поэтому декораторы комбинируются
        return Hit(hit.damage * MULTIPLIER, hit.critical)

    @property
    def experience_reward(self) -> int:
        return super().experience_reward * MULTIPLIER

    def roll_gold_reward(self) -> int:
        return super().roll_gold_reward() * MULTIPLIER