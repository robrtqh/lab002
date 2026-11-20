from unittest.mock import Mock

from lab3.defense.armor_handler import ArmorHandler
from lab3.defense.barrier_handler import BarrierHandler
from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler
from lab3.defense.evasion_handler import EvasionHandler


class RecordingHandler(DamageHandler):
    """Звено-шпион: записывает, что оно было вызвано, и передаёт урон дальше."""

    def __init__(self, name: str, log: list):
        super().__init__()
        self._name = name
        self._log = log

    def handle(self, damage: Damage) -> None:
        self._log.append(self._name)
        self._pass_to_next(damage)


def test_request_passes_through_all_handlers_in_order():
    log = []
    first = RecordingHandler("первое", log)
    first.set_next(RecordingHandler("второе", log)).set_next(RecordingHandler("третье", log))

    first.handle(Damage(10))

    assert log == ["первое", "второе", "третье"]


def test_last_handler_without_next_does_not_fail():
    log = []

    RecordingHandler("единственное", log).handle(Damage(10))

    assert log == ["единственное"]


def test_set_next_returns_next_handler_for_building_chains():
    first, second = RecordingHandler("a", []), RecordingHandler("b", [])

    assert first.set_next(second) is second


def test_full_chain_evasion_armor_barrier():
    # шанс уклонения 0: реальный Dice даёт гарантированно False, тест стабилен
    chain = EvasionHandler(0.0)
    chain.set_next(ArmorHandler(0.3)).set_next(BarrierHandler(30))
    damage = Damage(30)

    chain.handle(damage)

    # броня: 30 -> 21, барьер поглощает все 21
    assert damage.absorbed == 21
    assert damage.amount == 0
    assert not damage.evaded


def test_barrier_is_spent_by_first_hit_and_second_passes_partially():
    chain = ArmorHandler(0.3)
    chain.set_next(BarrierHandler(30))
    first, second = Damage(30), Damage(30)

    chain.handle(first)
    chain.handle(second)

    assert (first.absorbed, first.amount) == (21, 0)
    assert (second.absorbed, second.amount) == (9, 12)


def test_successful_evasion_stops_chain():
    # шанс 1.0: реальный Dice даёт гарантированно True
    chain = EvasionHandler(1.0)
    next_handler = Mock(spec=DamageHandler)
    chain.set_next(next_handler)
    damage = Damage(40)

    chain.handle(damage)

    assert damage.evaded
    assert damage.amount == 0
    next_handler.handle.assert_not_called()