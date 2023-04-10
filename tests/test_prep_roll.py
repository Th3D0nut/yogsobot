import pytest

from yogsobot.prep import prep_roll


def test_prep_roll():
    response, cleaned_input_expression = prep_roll(("d8", "d8", "d20"), "Jake")
    assert "Jake" in response
    assert cleaned_input_expression == "2d8 d20"

def test_prep_roll_returns_error_with_shit_input():
    response, cleaned_input_expression = prep_roll(("d", "ah", "d20"), "Jake")
    assert cleaned_input_expression is None
    assert response == "Must be of form <amount>d<side_amount>."
