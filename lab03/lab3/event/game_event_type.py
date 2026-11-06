from enum import Enum


class GameEventType(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    LEVEL_UP = "level-up"