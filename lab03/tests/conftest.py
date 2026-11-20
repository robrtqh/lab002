import pytest

from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item.default_catalog import DefaultCatalog


@pytest.fixture
def catalog():
    """Свежий каталог предметов для каждого теста."""
    return DefaultCatalog.create()


@pytest.fixture
def make_hero(catalog):
    """Фабрика героев: make_hero('Артур') или make_hero('Мерлин', HeroClass.MAGE)."""
    def _make(name="Артур", hero_class=HeroClass.WARRIOR):
        return (
            Hero.Builder()
            .set_name(name)
            .set_hero_class(hero_class)
            .set_starter_kit(hero_class.get_starter_kit(catalog))
            .build()
        )
    return _make