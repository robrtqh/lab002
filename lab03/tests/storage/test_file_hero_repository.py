import pytest

from lab3.hero.hero import Hero
from lab3.hero.hero_class import HeroClass
from lab3.item import enchantment
from lab3.item.default_catalog import DefaultCatalog
from lab3.progress.achievement import Achievement
from lab3.storage.file_hero_repository import FileHeroRepository


def test_restores_hero_through_new_repository(tmp_path, catalog):
    file = tmp_path / "heroes.json"
    writer = FileHeroRepository(file, catalog)
    original = (
        Hero.Builder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
        .set_level(2)
        .set_experience(35)
        .set_gold(175)
        .set_achievements([Achievement.FIRST_BLOOD])
        .build()
    )

    writer.save(original)
    # читаем НОВЫМ репозиторием: данные должны прийти из файла, а не из памяти писавшего
    reader = FileHeroRepository(file, DefaultCatalog.create())
    restored = reader.find_by_name("Артур")

    assert restored is not None
    assert restored is not original
    assert restored.name == "Артур"
    assert restored.hero_class == HeroClass.WARRIOR
    assert restored.level == 2
    assert restored.experience == 35
    assert restored.gold == 175
    assert restored.weapon.code == original.weapon.code
    assert restored.armor.code == original.armor.code
    assert restored.achievements == (Achievement.FIRST_BLOOD,)
    # текущее здоровье в файл не сохраняется, поэтому его не проверяем


def test_restores_enchanted_item_in_inventory(tmp_path, catalog):
    file = tmp_path / "heroes.json"
    sword = catalog.create(DefaultCatalog.IRON_SWORD)
    sword.enchant(enchantment.FIERY)
    hero = (
        Hero.Builder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
        .set_inventory([sword])
        .build()
    )
    FileHeroRepository(file, catalog).save(hero)

    restored = FileHeroRepository(file, DefaultCatalog.create()).find_by_name("Артур")

    assert len(restored.inventory) == 1
    assert restored.inventory[0].code == DefaultCatalog.IRON_SWORD
    assert restored.inventory[0].enchantments == (enchantment.FIERY,)


def test_missing_file_means_empty_storage(tmp_path, catalog):
    repository = FileHeroRepository(tmp_path / "missing.json", catalog)

    assert repository.find_all() == []
    assert repository.find_by_name("Артур") is None


def test_saving_existing_hero_replaces_record_instead_of_duplicating(tmp_path, catalog, make_hero):
    repository = FileHeroRepository(tmp_path / "heroes.json", catalog)
    arthur = make_hero("Артур")
    repository.save(arthur)
    repository.save(make_hero("Мерлин", HeroClass.MAGE))

    arthur.add_gold(100)
    repository.save(arthur)

    heroes = repository.find_all()
    assert sorted(hero.name for hero in heroes) == ["Артур", "Мерлин"]
    assert repository.find_by_name("Артур").gold == 150  # 50 стартовых + 100


def test_file_with_wrong_structure_is_rejected(tmp_path, catalog):
    file = tmp_path / "heroes.json"
    file.write_text("{}", encoding="utf-8")  # ожидается массив героев

    with pytest.raises(ValueError):
        FileHeroRepository(file, catalog).find_all()