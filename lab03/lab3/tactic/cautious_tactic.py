from lab3.tactic.action import Action
from lab3.tactic.tactic import Tactic

LOW_HEALTH = 0.4


class CautiousTactic(Tactic):
    @property
    def code(self):
        return "cautious"

    @property
    def display_name(self):
        return "Осторожность"

    @property
    def description(self):
        return "при здоровье ниже 40% через раунд уходить в оборону"

    def choose_action(self, round_number, hero, enemy):
        wounded = hero.health < hero.max_health * LOW_HEALTH
        return Action.DEFEND if wounded and round_number % 2 == 0 else Action.ATTACK