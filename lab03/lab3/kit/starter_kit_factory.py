from abc import ABC, abstractmethod

from lab3.item.armor import Armor
from lab3.item.weapon import Weapon


class StarterKitFactory(ABC):
    """Абстрактная фабрика: стартовый набор снаряжения."""

    @abstractmethod
    def create_weapon(self) -> Weapon:
        """Возвращает некое оружие."""

    @abstractmethod
    def create_armor(self) -> Armor:
        """Возвращает некую броню."""