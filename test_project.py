import pytest
from requests import patch

from project import get_word, game_begins, requests, get_word_meaning, get_valid_word_input, choose_difficulty_level


def test_get_word():
    word_length = 4
    word = get_word(word_length)
    assert len(word) == word_length

    word_length2 = 7
    assert len(word) != word_length2

def test_choose_difficulty_level(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2")
    correct_word, guess_tries = choose_difficulty_level()
    assert 5 <= len(correct_word) <= 8

def test_game_begins(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "apple")
    result = game_begins("APPLE",15)
    assert result == "Congratulations!\nThe word is: APPLE"

    monkeypatch.setattr('builtins.input', lambda _: "cake")
    result = game_begins("ONCE",10)
    assert result == "Game over! The word was: ONCE"


def test_get_valid_word_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "tree")
    assert get_valid_word_input("CAKE") == "TREE"


def test_get_word_meaning():
    response = requests.get("https://www.dictionary.com/browse/dog")

    assert response.status_code == 200

    try:
        get_word_meaning("worddoesn'texist")
    except Exception as exc:
        assert "Failed to retrieve page" in str(exc)


