from lab3.combat.hit import Hit
from lab3.enemy.enemy import Enemy
from lab3.enemy.enemy_decorator import EnemyDecorator

REWARD_BONUS_PERCENT = 50


class WindfuryEnemy(EnemyDecorator):
    """Неистовый: два броска урона складываются в один удар."""

    def __init__(self, wrapped: Enemy):
        super().__init__(wrapped)

    @property
    def name(self) -> str:
        return "Неистовый " + super().name

    def roll_damage(self) -> Hit:
        first = super().roll_damage()
        second = super().roll_damage()
        return Hit(first.damage + second.damage, first.critical or second.critical)

    @property
    def experience_reward(self) -> int:
        return self._with_bonus(super().experience_reward)

    def roll_gold_reward(self) -> int:
        return self._with_bonus(super().roll_gold_reward())

    @staticmethod
    def _with_bonus(reward: int) -> int:
        return reward + reward * REWARD_BONUS_PERCENT // 100