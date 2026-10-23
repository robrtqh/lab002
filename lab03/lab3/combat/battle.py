from lab3.combat.battle_event import BattleEvent
from lab3.combat.battle_report import BattleReport
from lab3.combat.combatant import Combatant
from lab3.combat.event_type import EventType
from lab3.combat.outcome import Outcome
from lab3.combat.participant import Participant
from lab3.combat.side import Side


class Battle:
    """Бой идёт по раундам: сначала бьёт герой, потом враг, пока кто-то не погибнет."""

    def __init__(self, hero: Combatant, enemy: Combatant):
        self._hero = hero
        self._enemy = enemy
        self._events: list[BattleEvent] = []
        self._round = 0

    def run(self) -> BattleReport:
        while self._hero.is_alive() and self._enemy.is_alive():
            self._round += 1
            self._strike(self._hero, Side.HERO, self._enemy, Side.ENEMY)
            if self._enemy.is_alive():
                self._strike(self._enemy, Side.ENEMY, self._hero, Side.HERO)

        outcome = Outcome.VICTORY if self._hero.is_alive() else Outcome.DEFEAT
        return BattleReport(
            Participant.of(self._hero),
            Participant.of(self._enemy),
            outcome,
            tuple(self._events),
        )

    def _strike(self, attacker: Combatant, source: Side, defender: Combatant, target: Side) -> None:
        hit = attacker.roll_damage()
        dealt = defender.receive_hit(hit.damage)
        event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
        self._events.append(BattleEvent(self._round, event_type, source, target, dealt, defender.health))

        if not defender.is_alive():
            self._events.append(BattleEvent(self._round, EventType.DEATH, source, target, 0, 0))