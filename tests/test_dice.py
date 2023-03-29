import pytest

from yogsobot.dice import roll_all

@pytest.mark.parametrize("input_dice, expected_len", [
    ({8: 2}, 2),
    ({6: 1, 10: 2, 8: 6}, 9),
])
def test_roll_all(input_dice, expected_len):
    results = roll_all(input_dice)
    assert len(results) == expected_len
