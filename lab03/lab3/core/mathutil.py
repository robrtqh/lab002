import math


def round_half_up(value: float) -> int:
    """Округление как в Java: 0.5 округляется вверх."""
    return int(math.floor(value + 0.5))