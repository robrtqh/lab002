from lab3.event.game_event import GameEvent
from lab3.event.game_event_listener import GameEventListener
from lab3.event.game_event_type import GameEventType
from lab3.progress.achievement import Achievement

VETERAN_LEVEL = 5


class AchievementTracker(GameEventListener):
    """Подписчик 1: выдаёт достижения."""

    def on_event(self, event: GameEvent) -> None:
        hero = event.hero
        if event.type == GameEventType.VICTORY:
            hero.unlock(Achievement.FIRST_BLOOD)

            if event.expedition.battle.enemy.code == "dragon":
                hero.unlock(Achievement.DRAGON_SLAYER)

            loot = event.expedition.rewards.loot
            if loot is not None and loot.enchantments:
                hero.unlock(Achievement.LUCKY)
        elif event.type == GameEventType.LEVEL_UP and hero.level >= VETERAN_LEVEL:
            hero.unlock(Achievement.VETERAN)