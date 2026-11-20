import pytest

from lab3.game.game_facade import GameFacade


def test_game_creates_hero_explores_and_saves(tmp_path):
    save_file = tmp_path / "game.json"
    game = GameFacade(save_file)
    game.create_hero("Гэндальф", "mage")

    report = game.explore("Гэндальф", "forest", "balanced")

    assert report.location_code == "forest"
    assert report.tactic_code == "balanced"
    assert save_file.exists()
    assert len(game.get_journal("Гэндальф")) == 1  # наблюдатель записал экспедицию


def test_hero_survives_game_restart(tmp_path):
    save_file = tmp_path / "game.json"
    GameFacade(save_file).create_hero("Гэндальф", "mage")

    restarted = GameFacade(save_file)  # «перезапуск игры»: новый фасад на том же файле

    assert [hero.name for hero in restarted.get_heroes()] == ["Гэндальф"]


def test_hero_with_same_name_is_rejected(tmp_path):
    game = GameFacade(tmp_path / "game.json")
    game.create_hero("Артур", "warrior")

    with pytest.raises(ValueError, match="уже есть"):
        game.create_hero("Артур", "ranger")