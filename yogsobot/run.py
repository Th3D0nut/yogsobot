import os
from sqlite3 import IntegrityError

import discord
from discord.ext import commands

from settings import TOKEN, ROOT, MY_ID 
from userinput.parse import parse_roll_expression, reverse_to_expression
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


@client.command()
async def roll(ctx, *expressions: str):  # Roll, keep short for easier command
    """
    Roll dice!

    Call this command with it's defined command prefix and the function name.
    Arguments can be of <amount_of_rolls>"d"<side_amount>.
    So for example '2d6' will roll two dice with six sides.
    """
    # Will hold a die with the number of times it should be rolled. Example: ([d]6: 8)
    dice_to_roll: dict[int, int] = {}
    for expression in expressions:
        try:
            die_amount, side_amount = parse_roll_expression(expression)
        except ValueError as error:
            await ctx.channel.send(error)
            return
        # Squash dice
        try:
            curr_saved_die_amount = dice_to_roll[side_amount] 
            dice_to_roll[side_amount] = curr_saved_die_amount + die_amount
        except KeyError:
            dice_to_roll[side_amount] = die_amount

    roll_results = []
    for side_amount, die_amount in dice_to_roll.items():
        roll_results.append(dice.roll(side_amount))

    end_result = sum(roll_results)

    response = f"{ctx.author.nick} rolled dice; the sum is {end_result}"
    await ctx.channel.send(response)

    roll_expression = reverse_to_expression(dice_to_roll)
    global roll_history
    roll_history = update_roll_history(
        roll_history, ctx.author.id, ctx.author.nick, roll_expression
        )


@client.command()
async def r(ctx, *expressions):
    """Shorthand for roll function."""
    await roll(ctx, *expressions)


@client.command()
async def shutdown(ctx):
    """Remote shutdown"""
    if MY_ID is None:
        raise TypeError("MY_ID cannot be None")
    if ctx.author.id == int(MY_ID):
        await client.close()


@client.command()
async def save(ctx, alias=None):
    """
    Alias and save the last rolled set of dice for a user.
    """
    if not alias:
        await ctx.channel.send("Alias for roll save?")
        alias_requester_id = ctx.author.id

        while True:
            msg = await client.wait_for('message')
            if alias_requester_id == ctx.author.id:
                alias = msg.content.strip()  # Strip to account for accidental spacebar strokes

    if " " in alias:
        raise ValueError("No whitespace in alias allowed")

    discord_id = ctx.author.id
    last_roll = None
    try:
        last_roll = " ".join(roll_history[discord_id]["expression"])
    except KeyError:
        return await ctx.channel.send("Previous roll not found for this user.")


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
