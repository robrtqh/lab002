import pytest

from lab3.defense.armor_handler import ArmorHandler
from lab3.defense.damage import Damage


@pytest.mark.parametrize(
    "incoming, defense, expected",
    [
        (30, 0.3, 21),   # обычный случай
        (10, 0.5, 5),
        (1, 0.9, 1),     # броня всегда пропускает хотя бы 1 урона
    ],
)
def test_reduces_damage_by_defense(incoming, defense, expected):
    handler = ArmorHandler(defense)
    damage = Damage(incoming)

    handler.handle(damage)

    assert damage.amount == expected
    assert not damage.evaded