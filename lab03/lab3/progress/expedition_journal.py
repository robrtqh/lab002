from lab3.event.game_event import GameEvent
from lab3.event.game_event_listener import GameEventListener


class ExpeditionJournal(GameEventListener):
    """Подписчик 2: записывает экспедиции в журнал."""

    def __init__(self):
        self._entries: dict[str, list] = {}

    def on_event(self, event: GameEvent) -> None:
        self._entries.setdefault(event.hero.name, []).append(event.expedition)

    def get_entries(self, hero_name: str) -> list:
        return list(self._entries.get(hero_name, []))