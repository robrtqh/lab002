from abc import ABC, abstractmethod
from typing import Optional

from lab3.defense.damage import Damage


class DamageHandler(ABC):
    """Звено цепочки обязанностей."""

    def __init__(self):
        self._next: Optional["DamageHandler"] = None

    def set_next(self, next_handler: "DamageHandler") -> "DamageHandler":
        self._next = next_handler
        return next_handler  # чтобы можно было строить цепочку подряд

    @abstractmethod
    def handle(self, damage: Damage) -> None: ...

    def _pass_to_next(self, damage: Damage) -> None:
        if self._next is not None:
            self._next.handle(damage)