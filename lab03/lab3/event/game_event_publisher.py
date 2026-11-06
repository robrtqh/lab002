from lab3.event.game_event import GameEvent
from lab3.event.game_event_listener import GameEventListener
from lab3.event.game_event_type import GameEventType


class GameEventPublisher:
    """Издатель: подписчики хранятся по типу события."""

    def __init__(self):
        self._listeners: dict[GameEventType, list[GameEventListener]] = {}

    def subscribe(self, event_type: GameEventType, listener: GameEventListener) -> None:
        self._listeners.setdefault(event_type, []).append(listener)

    def unsubscribe(self, event_type: GameEventType, listener: GameEventListener) -> None:
        subscribed = self._listeners.get(event_type)
        if subscribed and listener in subscribed:
            subscribed.remove(listener)

    def publish(self, event: GameEvent) -> None:
        for listener in list(self._listeners.get(event.type, [])):
            listener.on_event(event)