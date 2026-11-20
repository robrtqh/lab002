from unittest.mock import Mock

from lab3.storage.caching_hero_repository import CachingHeroRepository
from lab3.storage.hero_repository import HeroRepository


def test_does_not_touch_storage_until_first_read():
    storage = Mock(spec=HeroRepository)

    CachingHeroRepository(storage)

    assert storage.mock_calls == []  # к хранилищу не было ни одного обращения


def test_two_searches_read_storage_only_once(make_hero):
    storage = Mock(spec=HeroRepository)
    hero = make_hero("Артур")
    storage.find_all.return_value = [hero]  # задаём содержимое подставного хранилища
    cache = CachingHeroRepository(storage)

    first = cache.find_by_name("Артур")
    second = cache.find_by_name("Артур")

    assert first is hero
    assert second is first
    storage.find_all.assert_called_once()  # без кэша было бы 2 вызова


def test_missing_hero_does_not_trigger_reload():
    storage = Mock(spec=HeroRepository)
    storage.find_all.return_value = []
    cache = CachingHeroRepository(storage)

    assert cache.find_by_name("Никто") is None
    assert cache.find_by_name("Никто") is None

    storage.find_all.assert_called_once()


def test_find_all_uses_cache(make_hero):
    storage = Mock(spec=HeroRepository)
    arthur, merlin = make_hero("Артур"), make_hero("Мерлин")
    storage.find_all.return_value = [arthur, merlin]
    cache = CachingHeroRepository(storage)

    first = cache.find_all()
    second = cache.find_all()

    assert first == [arthur, merlin]
    assert second == first
    storage.find_all.assert_called_once()


def test_save_goes_to_storage_and_updates_loaded_cache(make_hero):
    storage = Mock(spec=HeroRepository)
    old_hero = make_hero("Артур")
    storage.find_all.return_value = [old_hero]
    cache = CachingHeroRepository(storage)
    assert cache.find_by_name("Артур") is old_hero  # кэш загружен

    updated = make_hero("Артур")
    updated.add_gold(100)
    cache.save(updated)

    storage.save.assert_called_once_with(updated)  # передали настоящему хранилищу
    assert cache.find_by_name("Артур") is updated  # и обновили кэш
    storage.find_all.assert_called_once()           # повторной загрузки не было


def test_save_new_hero_before_first_read_loads_storage_once(make_hero):
    storage = Mock(spec=HeroRepository)
    storage.find_all.return_value = []
    cache = CachingHeroRepository(storage)
    hero = make_hero("Артур")

    cache.save(hero)

    storage.save.assert_called_once_with(hero)
    assert cache.find_by_name("Артур") is hero
    storage.find_all.assert_called_once()