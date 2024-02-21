from random import randint


def roll(side_amount):
    """Returns a random number based on the amount of sides."""
    if side_amount > 1:
        return randint(1, side_amount)
    else:
        raise ValueError("The amount of sides need to be a minimum of two.")


def roll_all(dice_to_roll: dict[int, int]) -> list[int]:
    results = []
    for side_amount in dice_to_roll:
        for _ in range(dice_to_roll[side_amount]):
            results.append(roll(side_amount))
    return results

