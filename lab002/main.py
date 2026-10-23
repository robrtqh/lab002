from lab002.parrot import Parrot
from lab002.person import Person
from lab002.turtle import Turtle


def main() -> None:
    kesha = Parrot("Kesha", 2)
    zavala = Turtle("Zavala", 4)
    kesha.happyBirthday()  # возраст 2 -> 3

    jack = Person("Jack", kesha)
    john = Person("John")

    jack.getPetInfo()
    john.getPetInfo()

    john.setPet(zavala)
    john.getPetInfo()


if __name__ == "__main__":
    main()