from lab3.tactic.action import Action
from lab3.tactic.tactic import Tactic


class AggressiveTactic(Tactic):
    @property
    def code(self):
        return "aggressive"

    @property
    def display_name(self):
        return "Натиск"

    @property
    def description(self):
        return "совершать безрассудные удары, пока у врага больше здоровья, чем у героя"

    def choose_action(self, round_number, hero, enemy):
        return Action.POWER_STRIKE if enemy.health > hero.health else Action.ATTACK