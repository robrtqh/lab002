from enum import Enum


class EventType(Enum):
    HIT = "hit"
    CRITICAL_HIT = "critical_hit"
    EVADE = "evade"
    ABSORB = "absorb"
    POWER_STRIKE = "power_strike"
    DEFEND = "defend"
    DEATH = "death"