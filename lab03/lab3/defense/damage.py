class Damage:
    """Результат получения урона: сколько прошло, было ли уклонение, сколько поглощено."""

    def __init__(self, amount: int):
        self.amount = amount
        self.evaded = False
        self.absorbed = 0

    def reduce_to(self, amount: int) -> None:
        self.amount = amount

    def evade(self) -> None:
        self.amount = 0
        self.evaded = True

    def absorb(self, value: int) -> None:
        self.amount -= value
        self.absorbed += value