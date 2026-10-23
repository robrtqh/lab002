from lab002.animal import Animal


class Turtle(Animal):

    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def getAgeInHumanYears(self) -> int:
        if self.getAge() <= 0:
            return 0
        return 15 + (self.getAge() - 1) * 2

    def express(self) -> None:
        print("  _____     ____")
        print(" /      \\  |  o |")
        print("|        |/ ___\\|")
        print("|_________/")
        print("|_|_| |_|_|")
        print()