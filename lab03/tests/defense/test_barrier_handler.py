import pytest

from lab3.defense.barrier_handler import BarrierHandler
from lab3.defense.damage import Damage


@pytest.mark.parametrize(
    "incoming, absorbed, remaining",
    [
        (0, 0, 0),    # ноль отдельно от своего класса
        (10, 10, 0),  # меньше прочности
        (29, 29, 0),  # граница снизу
        (30, 30, 0),  # равен прочности
        (31, 30, 1),  # граница сверху
        (40, 30, 10), # больше прочности
    ],
)
def test_handles_damage_boundaries(incoming, absorbed, remaining):
    # Arrange: барьер прочностью 30 и входящий урон
    barrier = BarrierHandler(30)
    damage = Damage(incoming)

    # Act
    barrier.handle(damage)

    # Assert: ожидания берём из правила барьера, а не из кода
    assert damage.absorbed == absorbed
    assert damage.amount == remaining


def test_spends_capacity_across_hits():
    barrier = BarrierHandler(30)
    first, second, third = Damage(20), Damage(20), Damage(20)

    barrier.handle(first)
    barrier.handle(second)
    barrier.handle(third)

    assert first.absorbed == 20 and first.amount == 0, "Первый удар поглощается полностью"
    assert second.absorbed == 10 and second.amount == 10, "На второй осталось 10 прочности"
    assert third.absorbed == 0 and third.amount == 20, "Барьер уже исчерпан"