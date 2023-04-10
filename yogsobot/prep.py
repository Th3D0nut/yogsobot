from userinput.parse import (
    parse_roll_input,
    reverse_to_expression,
    )
import dice


def prep_roll(rolls: tuple[str, ...], display_name) -> tuple[str, str | None]:
    """Returns all the neccersary data to complete the discord !roll command."""
    try:
        # Will hold dice with the number of times it should be rolled. Example: ([d]6: 8)
        parsed_dice: dict[int, int] = parse_roll_input(rolls)
    except ValueError as error:
        return str(error), None

    results = dice.roll_all(parsed_dice)
    summed = sum(results)

    roll_expression = reverse_to_expression(parsed_dice)
    response = (
        f"> **{display_name}** rolled {roll_expression}\n"
        f"> Individual results are: {' + '.join([str(results) for results in results])}\n"
        f"> The sum is **{summed}**"
        )
    return response, roll_expression
