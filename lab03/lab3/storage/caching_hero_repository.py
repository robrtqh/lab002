from typing import Optional

from lab3.hero.hero import Hero
from lab3.storage.hero_repository import HeroRepository


class CachingHeroRepository(HeroRepository):
    """Заместитель: управляет доступом к настоящему хранилищу, кэшируя чтение."""

    def __init__(self, target: HeroRepository):
        self._target = target
        self._cache: Optional[dict] = None

    def find_by_name(self, name: str) -> Optional[Hero]:
        return self._cached().get(name)

    def find_all(self) -> list:
        return list(self._cached().values())

    def save(self, hero: Hero) -> None:
        self._target.save(hero)  # пишем в оба места, чтобы кэш не разошёлся с файлом
        self._cached()[hero.name] = hero

    def _cached(self) -> dict:
        if self._cache is None:  # ленивая загрузка: файл читается только при первом обращении
            self._cache = {hero.name: hero for hero in self._target.find_all()}
        return self._cache