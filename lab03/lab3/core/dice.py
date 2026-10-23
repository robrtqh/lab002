import random


class Dice:
    """Одиночка: общий источник случайности на всю игру."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._random = random.Random()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def reseed(self, seed: int) -> None:
        self._random.seed(seed)

    def next_seed(self) -> int:
        return self._random.randrange(1_000_000)

    def roll(self, min_value: int, max_value: int) -> int:
        return self._random.randint(min_value, max_value)

    def chance(self, probability: float) -> bool:
        return self._random.random() < probability

    def pick(self, options: list):
        return self._random.choice(options)