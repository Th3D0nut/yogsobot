import pytest

from yogsobot.userinput.history import update_roll_history


def test_add_new_item():
    history = {
        "12345678": {
            "nickname": "roflcopterman",
            "expression": "d8 d10",
        }
    }
    history = update_roll_history(history, "09876321", "rembestwaifu", "d12 d20")
    expected_history = {
        "12345678": {
            "nickname": "roflcopterman",
            "expression": "d8 d10",
        },
        "09876321": {
            "nickname": "rembestwaifu",
            "expression": "d12 d20",
        }
    }
    assert history == expected_history
