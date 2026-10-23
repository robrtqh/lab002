from abc import ABC, abstractmethod


class Pet(ABC):

    @abstractmethod
    def express(self) -> None:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getAge(self) -> int:
        pass

    @abstractmethod
    def getAgeInHumanYears(self) -> int:
        pass