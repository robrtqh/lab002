from lab3.combat.combatant import Combatant
from lab3.combat.hit import Hit
from lab3.defense.damage import Damage
from lab3.hero.hero_class import HeroClass
from lab3.item.armor import Armor
from lab3.item.item import Item
from lab3.item.weapon import Weapon
from lab3.kit.starter_kit_factory import StarterKitFactory
from lab3.progress.achievement import Achievement

MAX_NAME_LENGTH = 20
STARTING_GOLD = 50
HEALTH_PER_LEVEL = 15
DAMAGE_PER_LEVEL = 3
EXPERIENCE_PER_LEVEL = 100


class Hero(Combatant):
    def __init__(self, builder: "Hero.Builder"):
        self._name = builder.name
        self._hero_class = builder.hero_class
        self._level = builder.level
        self._experience = builder.experience
        self._gold = builder.gold
        self._weapon = builder.weapon
        self._armor = builder.armor
        self._inventory: list[Item] = list(builder.inventory)
        self._achievements: list[Achievement] = list(builder.achievements)
        self._defense = None
        self._health = 0
        self.rest()

    class Builder:
        def __init__(self):
            self.name = None
            self.hero_class = None
            self.weapon = None
            self.armor = None
            self.level = 1
            self.experience = 0
            self.gold = STARTING_GOLD
            self.inventory = []
            self.achievements = []

        def set_name(self, name):
            self.name = name
            return self

        def set_hero_class(self, hero_class):
            self.hero_class = hero_class
            return self

        def set_weapon(self, weapon):
            self.weapon = weapon
            return self

        def set_armor(self, armor):
            self.armor = armor
            return self

        def set_starter_kit(self, kit: StarterKitFactory):
            self.weapon = kit.create_weapon()
            self.armor = kit.create_armor()
            return self

        def set_level(self, level):
            self.level = level
            return self

        def set_experience(self, experience):
            self.experience = experience
            return self

        def set_gold(self, gold):
            self.gold = gold
            return self

        def set_inventory(self, inventory):
            self.inventory = list(inventory)
            return self

        def set_achievements(self, achievements):
            self.achievements = list(achievements)
            return self

        def build(self) -> "Hero":
            if self.name is None or not self.name.strip():
                raise ValueError("У героя должно быть имя")
            if len(self.name) > MAX_NAME_LENGTH:
                raise ValueError(f"Имя героя не может быть длиннее {MAX_NAME_LENGTH} символов")
            if self.hero_class is None:
                raise ValueError("Не выбран класс героя")
            if self.weapon is None or self.armor is None:
                raise ValueError("Герою нужны оружие и броня")
            if self.level < 1:
                raise ValueError("Уровень героя не может быть меньше 1")
            if self.experience < 0:
                raise ValueError("Опыта не может быть меньше нуля")
            if self.gold < 0:
                raise ValueError("Золота не может быть меньше нуля")
            return Hero(self)

    # --- бой ---

    def roll_damage(self) -> Hit:
        hit = self._weapon.roll_damage()
        return Hit(hit.damage + (self._level - 1) * DAMAGE_PER_LEVEL, hit.critical)

    def receive_hit(self, amount: int) -> Damage:
        damage = Damage(amount)
        self._defense.handle(damage)  # применение цепочки защиты
        self._health = max(0, self._health - damage.amount)
        return damage

    def is_alive(self) -> bool:
        return self._health > 0

    # --- поведение между экспедициями ---

    def rest(self) -> None:
        """Отдых: здоровье восстанавливается, цепочка защиты собирается заново (барьер восстанавливается)."""
        self._health = self.max_health
        self._defense = self._hero_class.create_defense(self._armor, self._level)

    def gain_experience(self, amount: int) -> int:
        self._experience += amount
        levels_gained = 0
        while self._experience >= self.experience_to_next_level:
            self._experience -= self.experience_to_next_level
            self._level += 1
            levels_gained += 1
        return levels_gained

    def add_gold(self, amount: int) -> None:
        self._gold += amount

    def spend_gold(self, amount: int) -> None:
        if amount > self._gold:
            raise RuntimeError(f"Не хватает золота: нужно {amount}, есть {self._gold}")
        self._gold -= amount

    def add_item(self, item: Item) -> None:
        self._inventory.append(item)

    def remove_item(self, item: Item) -> None:
        if item not in self._inventory:
            raise ValueError(f"В инвентаре нет предмета {item.name}")
        self._inventory.remove(item)

    def equip(self, item: Item) -> None:
        if isinstance(item, Weapon):
            self.remove_item(item)
            self._inventory.append(self._weapon)
            self._weapon = item
        elif isinstance(item, Armor):
            self.remove_item(item)
            self._inventory.append(self._armor)
            self._armor = item
            self._defense = self._hero_class.create_defense(self._armor, self._level)
        else:
            raise ValueError(f"Предмет нельзя экипировать: {item.name}")

    def unlock(self, achievement: Achievement) -> bool:
        if achievement in self._achievements:
            return False
        self._achievements.append(achievement)
        return True

    # --- свойства ---

    @property
    def code(self) -> str:
        return self._hero_class.code

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._health

    @property
    def max_health(self) -> int:
        return self._hero_class.base_health + (self._level - 1) * HEALTH_PER_LEVEL

    @property
    def hero_class(self) -> HeroClass:
        return self._hero_class

    @property
    def level(self) -> int:
        return self._level

    @property
    def experience(self) -> int:
        return self._experience

    @property
    def experience_to_next_level(self) -> int:
        return self._level * EXPERIENCE_PER_LEVEL

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def weapon(self) -> Weapon:
        return self._weapon

    @property
    def armor(self) -> Armor:
        return self._armor

    @property
    def inventory(self) -> tuple:
        return tuple(self._inventory)

    @property
    def achievements(self) -> tuple:
        return tuple(self._achievements)