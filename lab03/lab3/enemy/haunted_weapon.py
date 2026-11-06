from lab3.combat.hit import Hit
from lab3.core.dice import Dice
from lab3.defense.damage import Damage
from lab3.enemy.enemy import Enemy
from lab3.item.weapon import Weapon

HEALTH_PER_DAMAGE = 5  # за каждую единицу урона оружия полагается 5 здоровья


class HauntedWeapon(Enemy):
    """Адаптер: Weapon выглядит как Enemy."""

    def __init__(self, weapon: Weapon):
        self._weapon = weapon
        self._max_health = weapon.damage * HEALTH_PER_DAMAGE
        self._health = self._max_health

    @property
    def code(self) -> str:
        return "haunted-weapon"

    @property
    def name(self) -> str:
        return "Одержимый " + self._weapon.name

    def roll_damage(self) -> Hit:
        return self._weapon.roll_damage()  # логика оружия переиспользуется целиком

    def receive_hit(self, amount: int) -> Damage:
        damage = Damage(amount)  # а это адаптер реализует сам
        self._health = max(0, self._health - damage.amount)
        return damage

    def is_alive(self) -> bool:
        return self._health > 0

    @property
    def experience_reward(self) -> int:
        return self._weapon.price // 2

    def roll_gold_reward(self) -> int:
        return Dice.get_instance().roll(self._weapon.price // 4, self._weapon.price // 2)

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._max_health