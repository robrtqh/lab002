from abc import ABC, abstractmethod
from typing import Optional

from lab3.hero.hero import Hero


class HeroRepository(ABC):
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Hero]: ...

    @abstractmethod
    def find_all(self) -> list: ...

    @abstractmethod
    def save(self, hero: Hero) -> None: ...