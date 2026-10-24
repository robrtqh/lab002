from lab3.enemy.abstract_enemy import AbstractEnemy


class Goblin(AbstractEnemy):
    """Гоблин: самый простой враг, без особенностей."""

    def __init__(self):
        super().__init__("goblin", "Гоблин", 50, 6, 14, 40, 30)