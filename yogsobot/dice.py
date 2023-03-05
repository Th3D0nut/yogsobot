from random import randint

        
def roll(side_amount):
    if side_amount > 1:
        return randint(1, side_amount)
    else:
        raise ValueError("The amount of sides need to be a minimum of two.")


def roll_multiple(*args):
    result = []
    for sides in args:
        result.append(roll(side_amount=sides))
        
    return sum(result)
