from enum import Enum

from lab3.core.unknown_code_error import UnknownCodeError


class Achievement(Enum):
    FIRST_BLOOD = ("first-blood", "Первая кровь", "одержать первую победу")
    LUCKY = ("lucky", "Счастливчик", "найти зачарованный лут")
    VETERAN = ("veteran", "Ветеран", "достичь 5 уровня")
    DRAGON_SLAYER = ("dragon-slayer", "Драконоборец", "победить дракона")

    def __init__(self, code, display_name, description):
        self.code = code
        self.display_name = display_name
        self.description = description

    @staticmethod
    def by_code(code: str) -> "Achievement":
        for achievement in Achievement:
            if achievement.code == code:
                return achievement
        raise UnknownCodeError("Достижение", code)