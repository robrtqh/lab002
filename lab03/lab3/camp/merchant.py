from lab3.core.unknown_code_error import UnknownCodeError
from lab3.hero.hero import Hero
from lab3.item.item import Item
from lab3.item.item_catalog import ItemCatalog

SELL_PRICE_PERCENT = 50


class Merchant:
    """Продаёт предметы из каталога и скупает ненужное за половину цены."""

    def __init__(self, catalog: ItemCatalog, assortment: list):
        self._catalog = catalog
        self._assortment = list(assortment)

    def get_showcase(self) -> list:
        """Образцы товаров, чтобы показать их покупателю."""
        return [self._catalog.create(code) for code in self._assortment]

    def buy(self, hero: Hero, code: str) -> Item:
        if code not in self._assortment:
            raise UnknownCodeError("Товар", code)
        item = self._catalog.create(code)  # покупатель получает свою копию
        hero.spend_gold(item.price)
        hero.add_item(item)
        return item

    def sell(self, hero: Hero, item: Item) -> int:
        price = self.get_sell_price(item)
        hero.remove_item(item)
        hero.add_gold(price)
        return price

    def get_sell_price(self, item: Item) -> int:
        return item.price * SELL_PRICE_PERCENT // 100