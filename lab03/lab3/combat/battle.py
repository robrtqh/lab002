from lab3.combat.battle_event import BattleEvent
from lab3.combat.battle_report import BattleReport
from lab3.combat.combatant import Combatant
from lab3.combat.event_type import EventType
from lab3.combat.hit import Hit
from lab3.combat.outcome import Outcome
from lab3.combat.participant import Participant
from lab3.combat.side import Side
from lab3.core.mathutil import round_half_up
from lab3.tactic.action import Action
from lab3.tactic.tactic import Tactic


class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant, tactic: Tactic):
        self._hero = hero
        self._enemy = enemy
        self._tactic = tactic  # стратегия живёт весь бой, поэтому хранится в поле
        self._events: list[BattleEvent] = []
        self._round = 0

    def run(self) -> BattleReport:
        while self._hero.is_alive() and self._enemy.is_alive():
            self._round += 1
            # использование стратегии: действие зависит от выбранного алгоритма
            action = self._tactic.choose_action(self._round, self._hero, self._enemy)
            self._announce(action)

            self._strike(self._hero, Side.HERO, self._enemy, Side.ENEMY, action.attack_multiplier)
            if self._enemy.is_alive():
                self._strike(self._enemy, Side.ENEMY, self._hero, Side.HERO, action.incoming_multiplier)

        outcome = Outcome.VICTORY if self._hero.is_alive() else Outcome.DEFEAT
        return BattleReport(
            Participant.of(self._hero), Participant.of(self._enemy), outcome, tuple(self._events)
        )

    def _announce(self, action: Action) -> None:
        if action == Action.POWER_STRIKE:
            self._emit(EventType.POWER_STRIKE, Side.HERO, Side.ENEMY, 0, 0)
        elif action == Action.DEFEND:
            self._emit(EventType.DEFEND, Side.HERO, Side.HERO, 0, 0)

    def _strike(self, attacker: Combatant, source: Side, defender: Combatant,
                target: Side, multiplier: float) -> None:
        hit: Hit = attacker.roll_damage()
        amount = max(1, round_half_up(hit.damage * multiplier))
        damage = defender.receive_hit(amount)

        if damage.evaded:
            self._emit(EventType.EVADE, source, target, 0, defender.health)
            return
        if damage.absorbed > 0:
            self._emit(EventType.ABSORB, source, target, damage.absorbed, defender.health)
        if damage.amount > 0:
            event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
            self._emit(event_type, source, target, damage.amount, defender.health)

        if not defender.is_alive():
            self._emit(EventType.DEATH, source, target, 0, 0)

    def _emit(self, event_type, source, target, amount, health_after) -> None:
        self._events.append(BattleEvent(self._round, event_type, source, target, amount, health_after))