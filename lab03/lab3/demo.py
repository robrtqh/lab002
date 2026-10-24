from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item.default_catalog import DefaultCatalog

catalog = DefaultCatalog.create()
hero = Hero.Builder().set_name("Артур").set_hero_class(HeroClass.WARRIOR) \
    .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog)).build()
print(hero.name, hero.max_health, hero.gold)  # Артур 120 50
try:
    Hero.Builder().set_hero_class(HeroClass.MAGE).build()
except ValueError as e:
    print(e)  # У героя должно быть имя