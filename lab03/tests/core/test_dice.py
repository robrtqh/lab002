import pytest

from lab3.core.dice import Dice


@pytest.fixture(autouse=True)
def reset_sequence():
    """Перед каждым тестом задаём известный сид (аналог @BeforeEach).
    autouse=True: фикстура применяется ко всем тестам файла без указания в аргументах."""
    Dice.get_instance().reseed(2026)


def test_returns_same_instance():
    first = Dice.get_instance()

    second = Dice.get_instance()

    assert first is not None
    assert first is second  # идентичность ссылок, а не просто равенство


def test_constructor_does_not_create_second_instance():
    assert Dice() is Dice()
    assert Dice() is Dice.get_instance()


def test_rolls_stay_within_bounds():
    dice = Dice.get_instance()

    for _ in range(100):
        result = dice.roll(1, 6)

        assert 1 <= result <= 6, f"Бросок {result} вне диапазона [1, 6]"


def test_roll_with_equal_bounds_returns_single_value():
    assert Dice.get_instance().roll(7, 7) == 7


def test_certain_outcomes():
    dice = Dice.get_instance()

    for _ in range(100):
        assert dice.chance(0.0) is False, "При вероятности 0 ожидается False"
        assert dice.chance(1.0) is True, "При вероятности 1 ожидается True"


def test_pick_returns_only_element():
    item = object()

    assert Dice.get_instance().pick([item]) is item


def test_pick_returns_element_of_list():
    items = ["меч", "щит", "посох"]
    dice = Dice.get_instance()

    for _ in range(100):
        assert dice.pick(items) in items


def test_reseed_repeats_sequence():
    dice = Dice.get_instance()
    dice.reseed(42)
    first = [dice.roll(1, 100) for _ in range(10)]

    dice.reseed(42)
    repeated = [dice.roll(1, 100) for _ in range(10)]

    assert first == repeated


def test_different_seeds_give_different_sequences():
    dice = Dice.get_instance()
    dice.reseed(1)
    first = [dice.roll(1, 1_000_000) for _ in range(10)]

    dice.reseed(2)
    second = [dice.roll(1, 1_000_000) for _ in range(10)]

    assert first != second


def test_next_seed_is_within_expected_range():
    dice = Dice.get_instance()

    for _ in range(100):
        assert 0 <= dice.next_seed() < 1_000_000