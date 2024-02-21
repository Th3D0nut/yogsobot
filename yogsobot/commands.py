from sqlite3 import IntegrityError

from settings import client, MY_ID, PATH_TO_DB
from userinput.history import update_roll_history, get_last_roll
from prep import prep_roll
from database.transactions import DatabaseActor

db = DatabaseActor(PATH_TO_DB)
db.init_tables()

SAVE_EXIT_COMMANDS = ["q", "quit", "stop", "exit"]  # used in the save function
roll_history = {}  # Use update_roll_history to fill this


@client.command()
async def helpme(ctx):
    msg = """
    Commands:
        !helpme
            prints you this help menu. 

        !r <dice_amount>d<side_amount>
            Roll dice and recieve all the dice added together.
            Example: "!roll 2d8 d10", will roll two dice with eight sides and one die with 10 sides.
    """
    await ctx.channel.send(msg)


@client.command()
async def shutdown(ctx) -> None:
    """Remote shutdown"""
    if MY_ID is None:
        raise TypeError("MY_ID cannot be None")
    if ctx.author.id == int(MY_ID):
        await client.close()  # client is global


@client.command(pass_context=True, aliases=["r"])
async def roll(ctx, *expressions: str) -> None:
    """
    Roll dice!

    Call this command with it's defined command prefix and the function name.
    Arguments can be of <amount_of_rolls>"d"<side_amount>.
    So for example '2d6' will roll two dice with six sides.
    """
    response, cleaned_input_expression = prep_roll(expressions, ctx.author.display_name)

    if cleaned_input_expression is not None:
        global roll_history
        roll_history = update_roll_history(
            roll_history,
            ctx.author.id,
            ctx.author.display_name,
            cleaned_input_expression
        )

    await ctx.channel.send(response)


@client.command()
async def save(ctx, alias: str | None = None) -> None:
    """
    Alias and save the last rolled set of dice for a user.
    """
    if alias is None:
        error_text = "An alias has to be given, try again like so: '!save <alias>'."
        await ctx.channel.send(error_text)
        raise TypeError(error_text)

    if " " in alias:
        error_text = "No whitespace in alias allowed"
        await ctx.channel.send(error_text)
        raise ValueError(error_text)

    last_roll: str = get_last_roll(roll_history, discord_id=ctx.author.id)
    if last_roll == "":
        return await ctx.channel.send("Roll history not found. Roll some dice first!")

    try:
        db.save_user(ctx.author.id)
    except IntegrityError:
        # Do nothing when user a:w
        # lready exists
        pass
    if last_roll is not None:
        db.save_roll(ctx.author.id, alias, last_roll)


@client.command()
async def cast(ctx, alias):
    roll_expression = db.get_roll(ctx.author.id, alias)
    if roll_expression is not None:
        await roll(ctx, *roll_expression.split())
    else:
        await ctx.channel.send("No alias found to cast.\nRoll and Save one first!")


@client.command()
async def view(ctx):
    aliases: list[tuple[str, str]] | None = db.get_all_aliases(ctx.author.id)
    if aliases is not None:
        response = (
            f"> **Aliases of {ctx.author.display_name}**\n"
            f"> {aliases[0][0]}: {aliases[0][1]}"
        )
        for alias, expression in aliases[1:]:
            response = f"{response}\n> {alias}: {expression}"
        await ctx.channel.send(response)
    else:
        ctx.channel.send(f"No aliases found for {ctx.author.display_name}.")
