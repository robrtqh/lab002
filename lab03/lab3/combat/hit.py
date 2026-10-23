from dataclasses import dataclass


@dataclass(frozen=True)
class Hit:
    """Удар: сколько урона и был ли он критическим."""
    damage: int
    critical: bool