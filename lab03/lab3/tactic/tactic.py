from abc import ABC, abstractmethod

from lab3.combat.combatant import Combatant
from lab3.tactic.action import Action


class Tactic(ABC):
    """Стратегия: как герой ведёт себя в бою."""

    @property
    @abstractmethod
    def code(self) -> str: ...

    @property
    @abstractmethod
    def display_name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def choose_action(self, round_number: int, hero: Combatant, enemy: Combatant) -> Action: ...