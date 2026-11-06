from lab3.defense.damage import Damage
from lab3.enemy.enemy import Enemy
from lab3.enemy.enemy_decorator import EnemyDecorator


class ArmoredEnemy(EnemyDecorator):
    """Бронированный: входящий урон уменьшается вдвое и передаётся дальше по цепочке."""

    def __init__(self, wrapped: Enemy):
        super().__init__(wrapped)

    @property
    def name(self) -> str:
        return "Бронированный " + super().name

    def receive_hit(self, amount: int) -> Damage:
        if amount < 0:
            raise ValueError("Урон не может быть отрицательным")
        if amount == 0:
            return Damage(0)
        return super().receive_hit(amount - amount // 2)