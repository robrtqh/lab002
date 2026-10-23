from abc import ABC, abstractmethod

from lab3.combat.hit import Hit


class Combatant(ABC):
    """Всё, что может участвовать в бою: и герой, и враги."""

    @property
    @abstractmethod
    def code(self) -> str:
        """Код вида сущности: класс героя или тип врага."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @property
    @abstractmethod
    def max_health(self) -> int: ...

    @abstractmethod
    def is_alive(self) -> bool: ...

    @abstractmethod
    def roll_damage(self) -> Hit:
        """Удар, который будет нанесён данной сущностью."""

    @abstractmethod
    def receive_hit(self, damage: int) -> int:
        """Получение удара, возвращает урон, который прошёл на самом деле."""