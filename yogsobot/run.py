import os
from sqlite3 import IntegrityError

import discord
from discord.ext import commands

from settings import TOKEN, ROOT, MY_ID 
from userinput.parse import (
    parse_roll_input,
    reverse_to_expression,
    )
from userinput.history import update_roll_history
from database.transactions import DatabaseActor
import dice

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

roll_history = {}  # Use update_roll_history to fill this

PATH_TO_DB = os.path.join(ROOT, "aliasroll.db")
db = DatabaseActor(PATH_TO_DB)
db.init_tables()

SAVE_EXIT_COMMANDS= ["q", "quit", "stop", "exit"]  # used in the save function


@client.event
async def on_ready():
    print(f"{client.user} has joined the server!")


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


@client.command(pass_context=True, aliases=["r"])
async def roll(ctx, *expressions: str) -> None:
    """
    Roll dice!

    Call this command with it's defined command prefix and the function name.
    Arguments can be of <amount_of_rolls>"d"<side_amount>.
    So for example '2d6' will roll two dice with six sides.
    """
    try:
        # Will hold dice with the number of times it should be rolled. Example: ([d]6: 8)
        dice_to_roll = parse_roll_input(expressions)
    except ValueError as error:
        await ctx.channel.send(error)
        return

    results = dice.roll_all(dice_to_roll)
    summed = sum(results)

    roll_expression = reverse_to_expression(dice_to_roll)
    response = (
        f"> **{ctx.author.display_name}** rolled {roll_expression}\n"
        f"> Individual results are: {' + '.join([str(results) for results in results])}\n"
        f"> The sum is **{summed}**"
        )
    await ctx.channel.send(response)

    global roll_history
    roll_history = update_roll_history(
        roll_history, ctx.author.id, ctx.author.display_name, roll_expression
        )


@client.command()
async def shutdown(ctx) -> None:
    """Remote shutdown"""
    if MY_ID is None:
        raise TypeError("MY_ID cannot be None")
    if ctx.author.id == int(MY_ID):
        await client.close()  # client is global


@client.command()
async def save(ctx, alias: str | None = None) -> None:
    """
    Alias and save the last rolled set of dice for a user.

    When no alias is passed a user will be prompted to send one.
    """
    # Check if alias exist; otherwise prompt user for one
    if not alias:
        await ctx.channel.send("Alias for roll save?")
        alias_requester_id = ctx.author.id

        while True:
            msg = await client.wait_for('message')
            if alias_requester_id == ctx.author.id:
                alias = msg.content.strip()  # Strip to account for accidental spacebar strokes
                if alias in SAVE_EXIT_COMMANDS:  # Global variable
                    await ctx.channel.send("Exit command given, not storing command")
                    return

    if " " in alias:
        error_text = "No whitespace in alias allowed"
        await ctx.channel.send(error_text)
        raise ValueError(error_text)

    discord_id = ctx.author.id
    last_roll = None
    try:
        last_roll = roll_history[discord_id]["expression"]
    except KeyError:
        return await ctx.channel.send("Roll history not found. Roll some dice first!")

    try:
        db.save_user(discord_id)
    except IntegrityError:
        # Do nothing when user already exists
        pass
    if last_roll is not None:
        db.save_roll(discord_id, alias, last_roll)


@client.command()
async def cast(ctx, alias):
    await roll(ctx, *db.get_roll(ctx.author.id, alias).split())


if __name__ == "__main__":
    if TOKEN is None:
        raise TypeError(
            "TOKEN cannot be None and has to be of string containing a discord token."
            )
    client.run(TOKEN)
