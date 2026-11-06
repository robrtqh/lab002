from lab3.tactic.action import Action
from lab3.tactic.tactic import Tactic


class BalancedTactic(Tactic):
    @property
    def code(self):
        return "balanced"

    @property
    def display_name(self):
        return "Баланс"

    @property
    def description(self):
        return "обычный удар каждый раунд"

    def choose_action(self, round_number, hero, enemy):
        return Action.ATTACK