from abc import ABC, abstractmethod

from lab3.event.game_event import GameEvent


class GameEventListener(ABC):
    @abstractmethod
    def on_event(self, event: GameEvent) -> None: ...