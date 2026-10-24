from abc import abstractmethod

from lab3.combat.combatant import Combatant


class Enemy(Combatant):
    @property
    @abstractmethod
    def experience_reward(self) -> int: ...

    @abstractmethod
    def roll_gold_reward(self) -> int: ...