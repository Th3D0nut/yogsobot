import pytest

from yogsobot.userinput.parse import parse_roll_expression


@pytest.mark.parametrize("expression, expected_dice, expected_sides", [
    ("d6", 1, 6),  # normal roll
    ("1d6", 1, 6),  # alternative
    ("d20", 1, 20),  # another normal roll
    ("2d6", 2, 6),  # rolling two dice
    ("1d2", 1, 2),  # smallest die en amount of dice thrown
    ("30d100", 30, 100),  # biggest die en amount of dice thrown
])
def test_parse_die_expression_with_accepted_input(
    expression, expected_dice, expected_sides
    ):
    dice, sides = parse_roll_expression(expression)
    assert dice == expected_dice
    assert sides == expected_sides


@pytest.mark.parametrize("expression", [
    ("f5"),  # should only accept d
    ("d0"),  # makes no sense to roll this
    ("0d6"),  # makes no sense too
    ("d1"),  # too little sides
    ("d101"),  # too many sides
])
def test_throws_value_error_with_unaccepted_input(expression):
    with pytest.raises(ValueError):
        parse_roll_expression(expression)
