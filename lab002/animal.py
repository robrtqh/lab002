from abc import abstractmethod

from lab002.pet import Pet


class Animal(Pet):

    def __init__(self, name: str, age: int):
        self.__name = name
        self.__age = age

    def happyBirthday(self) -> None:
        self.__age += 1

    @abstractmethod
    def express(self) -> None:
        pass

    @abstractmethod
    def getAgeInHumanYears(self) -> int:
        pass

    def getName(self) -> str:
        return self.__name

    def getAge(self) -> int:
        return self.__age