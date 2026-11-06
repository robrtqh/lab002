import json
from pathlib import Path
from typing import Optional

from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item.enchantment import Enchantment
from lab3.item.item import Item
from lab3.item.item_catalog import ItemCatalog
from lab3.progress.achievement import Achievement
from lab3.storage.hero_repository import HeroRepository


class FileHeroRepository(HeroRepository):
    """Реальное хранилище: массив героев в JSON-файле. Каждый запрос читает файл целиком."""

    def __init__(self, file: Path, catalog: ItemCatalog):
        self._file = Path(file)
        self._catalog = catalog

    def find_by_name(self, name: str) -> Optional[Hero]:
        for hero in self.find_all():
            if hero.name == name:
                return hero
        return None

    def find_all(self) -> list:
        if not self._file.exists():
            return []
        text = self._file.read_text(encoding="utf-8")
        if not text.strip():
            return []
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"Ожидался массив героев: {self._file.resolve()}")
        return [self._restore(entry) for entry in data]

    def save(self, hero: Hero) -> None:
        saves = [self._snapshot(saved) for saved in self.find_all() if saved.name != hero.name]
        saves.append(self._snapshot(hero))
        self._file.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(saves, ensure_ascii=False, indent=2) + "\n"
        self._file.write_text(text, encoding="utf-8")

    @staticmethod
    def _snapshot_item(item: Item) -> dict:
        return {"code": item.code, "enchantments": [e.code for e in item.enchantments]}

    def _snapshot(self, hero: Hero) -> dict:
        return {
            "name": hero.name,
            "heroClass": hero.hero_class.code,
            "level": hero.level,
            "experience": hero.experience,
            "gold": hero.gold,
            "weapon": self._snapshot_item(hero.weapon),
            "armor": self._snapshot_item(hero.armor),
            "inventory": [self._snapshot_item(item) for item in hero.inventory],
            "achievements": [a.code for a in hero.achievements],
        }

    def _restore_item(self, data: dict, weapon=False, armor=False) -> Item:
        if weapon:
            item = self._catalog.create_weapon(data["code"])
        elif armor:
            item = self._catalog.create_armor(data["code"])
        else:
            item = self._catalog.create(data["code"])
        for code in data["enchantments"]:
            item.enchant(Enchantment.by_code(code))
        return item

    def _restore(self, data: dict) -> Hero:
        return (
            Hero.Builder()
            .set_name(data["name"])
            .set_hero_class(HeroClass.by_code(data["heroClass"]))
            .set_level(data["level"])
            .set_experience(data["experience"])
            .set_gold(data["gold"])
            .set_weapon(self._restore_item(data["weapon"], weapon=True))
            .set_armor(self._restore_item(data["armor"], armor=True))
            .set_inventory([self._restore_item(i) for i in data["inventory"]])
            .set_achievements([Achievement.by_code(c) for c in data["achievements"]])
            .build()
        )