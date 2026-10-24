from lab3.core.unknown_code_error import UnknownCodeError
from lab3.world.location import Location


class LocationRegistry:
    """Все локации игры."""

    def __init__(self, locations: list):
        self._locations = {location.code: location for location in locations}

    def get(self, code: str) -> Location:
        location = self._locations.get(code)
        if location is None:
            raise UnknownCodeError("Локация", code)
        return location

    def get_all(self) -> list:
        return list(self._locations.values())