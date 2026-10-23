from lab002.animal import Animal


class Parrot(Animal):

    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def getAgeInHumanYears(self) -> int:
        return self.getAge() * 5

    def express(self) -> None:
        print(f'{self.getName()}: "Hello!"')
        print("   \\")
        print("   (o>")
        print("\\\\_//)")
        print(" \\_/_)")
        print("  _|_")
        print()