from unittest.mock import Mock

import pytest

from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item.default_catalog import DefaultCatalog
from lab3.kit.starter_kit_factory import StarterKitFactory


@pytest.fixture
def valid_builder(catalog):
    """Строитель с заполненными обязательными полями."""
    return (
        Hero.Builder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
    )


def test_builds_hero_with_defaults(valid_builder):
    hero = valid_builder.build()

    assert hero.name == "Артур"
    assert hero.level == 1
    assert hero.experience == 0
    assert hero.gold == 50
    assert hero.health == hero.max_health == 120
    assert hero.inventory == ()
    assert hero.achievements == ()


def test_setters_return_builder_for_chaining():
    builder = Hero.Builder()

    assert builder.set_name("Артур") is builder
    assert builder.set_level(3) is builder


def test_optional_fields_are_applied(valid_builder):
    hero = valid_builder.set_level(3).set_gold(175).set_experience(20).build()

    assert hero.level == 3
    assert hero.gold == 175
    assert hero.experience == 20
    assert hero.max_health == 120 + 2 * 15  # здоровье растёт с уровнем


def test_starter_kit_is_taken_from_factory(catalog):
    weapon = catalog.create_weapon(DefaultCatalog.TRAINING_SWORD)
    armor = catalog.create_armor(DefaultCatalog.CHAINMAIL)
    kit = Mock(spec=StarterKitFactory)  # подставная абстрактная фабрика
    kit.create_weapon.return_value = weapon
    kit.create_armor.return_value = armor

    hero = Hero.Builder().set_name("Артур").set_hero_class(HeroClass.WARRIOR).set_starter_kit(kit).build()

    kit.create_weapon.assert_called_once()
    kit.create_armor.assert_called_once()
    assert hero.weapon is weapon
    assert hero.armor is armor


@pytest.mark.parametrize("name", [None, "", "   "])
def test_rejects_missing_or_blank_name(valid_builder, name):
    valid_builder.set_name(name)

    with pytest.raises(ValueError, match="имя"):
        valid_builder.build()


def test_rejects_too_long_name(valid_builder):
    valid_builder.set_name("а" * 21)

    with pytest.raises(ValueError, match="длиннее"):
        valid_builder.build()


def test_accepts_name_of_maximum_length(valid_builder):
    assert valid_builder.set_name("а" * 20).build().name == "а" * 20


def test_rejects_missing_hero_class(catalog):
    builder = Hero.Builder().set_name("Артур").set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))

    with pytest.raises(ValueError, match="класс"):
        builder.build()


def test_rejects_missing_equipment():
    builder = Hero.Builder().set_name("Артур").set_hero_class(HeroClass.WARRIOR)

    with pytest.raises(ValueError, match="оружие"):
        builder.build()


@pytest.mark.parametrize(
    "setter, value, message",
    [
        ("set_level", 0, "Уровень"),
        ("set_gold", -1, "Золота"),
        ("set_experience", -1, "Опыта"),
    ],
)
def test_rejects_invalid_numbers(valid_builder, setter, value, message):
    getattr(valid_builder, setter)(value)

    with pytest.raises(ValueError, match=message):
        valid_builder.build()