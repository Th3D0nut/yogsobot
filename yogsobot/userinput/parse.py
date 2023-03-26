def parse_roll_expression(expression: str) -> tuple[int, int]:
    """From a string describing a dice roll, return the amount of dice and sides"""
    try:
        dice_amount, side_amount = expression.lower().split("d")
    except ValueError:
        raise ValueError("Must be of form <amount>d<side_amount>.")

    # enter a 1 before d<number> or parse it as is
    if dice_amount:  # account for empty string
        dice_amount = int(dice_amount)
    else:
        dice_amount = 1

    side_amount = int(side_amount)

    if not 1 <= dice_amount <= 30:
        raise ValueError(
            "The amount of dice has to be between one and thirty."
            )
    if not 2 <= side_amount <= 100:
        raise ValueError(
            "The amount of sides of the die have to be between two and a hundred"
            )
    return dice_amount, side_amount
