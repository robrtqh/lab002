from unittest.mock import Mock, patch

from lab3.core.dice import Dice
from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler
from lab3.defense.evasion_handler import EvasionHandler

DICE_PATH = "lab3.defense.evasion_handler.Dice"  # где Dice ищется, там и подменяем


def make_dice(chance_result: bool) -> Mock:
    """Подставной кубик: метод chance всегда возвращает заданный результат."""
    dice = Mock(spec=Dice)  # spec: у мока только методы настоящего Dice
    dice.chance.return_value = chance_result
    return dice


def test_successful_roll_zeroes_damage_and_stops_chain():
    dice = make_dice(True)
    handler = EvasionHandler(0.3)  # настоящий обработчик, мокируем только зависимости
    next_handler = Mock(spec=DamageHandler)
    handler.set_next(next_handler)
    damage = Damage(40)

    with patch(DICE_PATH) as dice_class:  # подмена действует только внутри блока with
        dice_class.get_instance.return_value = dice
        handler.handle(damage)

        dice_class.get_instance.assert_called_once()

    assert damage.amount == 0
    assert damage.evaded is True
    dice.chance.assert_called_once_with(0.3)
    next_handler.handle.assert_not_called()  # следующее звено не вызывали


def test_failed_roll_forwards_damage_to_next_handler():
    dice = make_dice(False)
    handler = EvasionHandler(0.3)
    next_handler = Mock(spec=DamageHandler)
    handler.set_next(next_handler)
    damage = Damage(40)

    with patch(DICE_PATH) as dice_class:
        dice_class.get_instance.return_value = dice
        handler.handle(damage)

    assert damage.amount == 40
    assert damage.evaded is False
    dice.chance.assert_called_once_with(0.3)
    next_handler.handle.assert_called_once_with(damage)  # тот же объект Damage


def test_failed_roll_without_next_handler_does_not_fail():
    handler = EvasionHandler(0.3)
    damage = Damage(40)

    with patch(DICE_PATH) as dice_class:
        dice_class.get_instance.return_value = make_dice(False)
        handler.handle(damage)

    assert damage.amount == 40