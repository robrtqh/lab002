from lab3.hero.hero_class import HeroClass
from lab3.item.default_catalog import DefaultCatalog

catalog = DefaultCatalog.create()
for hero_class in HeroClass:
    kit = hero_class.get_starter_kit(catalog)
    weapon, armor = kit.create_weapon(), kit.create_armor()
    print(f"{hero_class.display_name}: {weapon.name} ({weapon.description}), {armor.name} ({armor.description})")