from lab3.item.default_catalog import DefaultCatalog
from lab3.item import enchantment

catalog = DefaultCatalog.create()
a = catalog.create(DefaultCatalog.IRON_SWORD)
b = catalog.create(DefaultCatalog.IRON_SWORD)
b.enchant(enchantment.FIERY)

print(a.name, a.description)  # Железный меч урон 17
print(b.name, b.description)  # Железный меч урон 23
print(catalog.create(DefaultCatalog.IRON_SWORD).description)  # урон 17, шаблон не изменился
print(a is not b)  # True