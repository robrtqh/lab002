from unittest.mock import Mock

import pytest

from lab3.combat.hit import Hit
from lab3.defense.damage import Damage
from lab3.enemy.armored_enemy import ArmoredEnemy
from lab3.enemy.enemy import Enemy
from lab3.enemy.enemy_decorator import EnemyDecorator
from lab3.enemy.goblin import Goblin
from lab3.enemy.legendary_enemy import LegendaryEnemy
from lab3.enemy.windfury_enemy import WindfuryEnemy


@pytest.fixture
def wrapped():
    """Подставной враг, вместо настоящего: все его ответы задаём сами."""
    enemy = Mock(spec=Enemy)
    enemy.name = "Гоблин"
    enemy.code = "goblin"
    enemy.health = 30
    enemy.max_health = 50
    enemy.experience_reward = 40
    enemy.is_alive.return_value = True
    enemy.roll_gold_reward.return_value = 30
    enemy.roll_damage.return_value = Hit(10, False)
    return enemy


# --- базовый декоратор ---

def test_base_decorator_delegates_everything_to_wrapped(wrapped):
    decorator = EnemyDecorator(wrapped)

    assert decorator.name == "Гоблин"
    assert decorator.code == "goblin"
    assert decorator.health == 30
    assert decorator.max_health == 50
    assert decorator.experience_reward == 40
    assert decorator.is_alive() is True
    assert decorator.roll_gold_reward() == 30
    assert decorator.roll_damage() == Hit(10, False)


# --- LegendaryEnemy ---

def test_legendary_doubles_damage(wrapped):
    hit = LegendaryEnemy(wrapped).roll_damage()

    assert hit.damage == 20
    assert hit.critical is False
    wrapped.roll_damage.assert_called_once()  # обёрнутый враг тоже был вызван


def test_legendary_keeps_critical_flag(wrapped):
    wrapped.roll_damage.return_value = Hit(10, True)

    assert LegendaryEnemy(wrapped).roll_damage().critical is True


def test_legendary_doubles_rewards(wrapped):
    enemy = LegendaryEnemy(wrapped)

    assert enemy.experience_reward == 80
    assert enemy.roll_gold_reward() == 60


def test_legendary_adds_name_prefix(wrapped):
    assert LegendaryEnemy(wrapped).name == "Легендарный Гоблин"


# --- WindfuryEnemy ---

def test_windfury_sums_two_rolls_into_one_hit(wrapped):
    wrapped.roll_damage.side_effect = [Hit(7, False), Hit(10, True)]

    hit = WindfuryEnemy(wrapped).roll_damage()

    assert hit.damage == 17
    assert hit.critical is True  # критический, если хотя бы один бросок критический
    assert wrapped.roll_damage.call_count == 2


def test_windfury_adds_half_to_rewards(wrapped):
    enemy = WindfuryEnemy(wrapped)

    assert enemy.experience_reward == 60  # 40 + 50%
    assert enemy.roll_gold_reward() == 45  # 30 + 50%


# --- ArmoredEnemy ---

@pytest.mark.parametrize("incoming, passed", [(20, 10), (15, 8), (2, 1), (1, 1)])
def test_armored_halves_incoming_damage(wrapped, incoming, passed):
    wrapped.receive_hit.return_value = Damage(passed)

    result = ArmoredEnemy(wrapped).receive_hit(incoming)

    wrapped.receive_hit.assert_called_once_with(passed)
    assert result is wrapped.receive_hit.return_value


def test_armored_ignores_zero_damage(wrapped):
    result = ArmoredEnemy(wrapped).receive_hit(0)

    assert result.amount == 0
    wrapped.receive_hit.assert_not_called()


def test_armored_rejects_negative_damage(wrapped):
    with pytest.raises(ValueError):
        ArmoredEnemy(wrapped).receive_hit(-5)


# --- комбинации ---

def test_stacked_decorators_all_take_part(wrapped):
    wrapped.roll_damage.side_effect = [Hit(5, False), Hit(6, True)]
    enemy = LegendaryEnemy(WindfuryEnemy(wrapped))

    hit = enemy.roll_damage()

    # неистовый: 5 + 6 = 11, легендарный: 11 * 2 = 22
    assert hit.damage == 22
    assert hit.critical is True
    assert wrapped.roll_damage.call_count == 2


def test_stacked_decorators_combine_rewards(wrapped):
    enemy = LegendaryEnemy(WindfuryEnemy(wrapped))

    assert enemy.experience_reward == 120  # 40 -> 60 (неистовый) -> 120 (легендарный)


def test_stacked_names_are_built_from_outside_in(wrapped):
    enemy = ArmoredEnemy(WindfuryEnemy(LegendaryEnemy(wrapped)))

    assert enemy.name == "Бронированный Неистовый Легендарный Гоблин"


def test_decorators_keep_enemy_code(wrapped):
    assert ArmoredEnemy(LegendaryEnemy(wrapped)).code == "goblin"


def test_incoming_damage_travels_through_whole_stack_to_real_enemy():
    goblin = Goblin()  # настоящий враг: 50 здоровья, брони нет
    enemy = ArmoredEnemy(LegendaryEnemy(goblin))

    result = enemy.receive_hit(20)

    assert result.amount == 10  # бронированный: 20 -> 10
    assert goblin.health == 40
    assert enemy.health == 40