from random import randint

        
def roll(side_amount):
    """Returns a random number based on the amount of sides."""
    if side_amount > 1:
        return randint(1, side_amount)
    else:
        raise ValueError("The amount of sides need to be a minimum of two.")


def roll_multiple(*side_amounts):
    """Returns the sum of multiple dice rolls."""
    result = []
    for side_amount in side_amounts:
        result.append(roll(side_amount=side_amount))
        
    return sum(result)
