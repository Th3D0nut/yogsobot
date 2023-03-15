import sqlite3
from os.path import join

import discord
from discord.ext import commands

from settings import TOKEN, ROOT, MY_ID 
from userinput.parse import parse_roll_expression
from database.utills import init_tables, save_user
import dice

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

roll_history = []  # Roll function fills this

PATH_TO_DB = join(ROOT, "aliasroll.db")
db_connection = sqlite3.connect(PATH_TO_DB)
db_curs = db_connection.cursor()
init_tables(db_curs)


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
async def r(ctx, *expressions):  # Roll, keep short for easier command
    """
    Roll dice!

    Call this command with it's defined command prefix and the function name.
    Arguments can be of <amount_of_rolls>"d"<side_amount>.
    So for example '2d6' will roll two dice with six sides.
    """
    rolled_dice = []
    for expression in expressions:
        try:
            dice_amount, side_amount = parse_roll_expression(expression)
        except ValueError as error:
            await ctx.channel.send(error)
            return

        for _ in range(dice_amount):
            rolled_dice.append(dice.roll(side_amount=side_amount))

    result = sum(rolled_dice)
    dice_rolls = " ".join(expressions)
    dice_results = " + ".join([str(die) for die in rolled_dice])
    response = (f"> **{ctx.author.nick}** rolled {dice_rolls}\n" \
            f"> {dice_results} is **{result}**")
    await ctx.channel.send(response)

    roll_history.append({
            "id": ctx.author.id,
            "nickname": ctx.author.nick,
            "expression": expressions,
        })


@client.command()
async def shutdown(ctx):
    """Remote shutdown"""
    if ctx.author.id == int(MY_ID):
        await client.close()


@client.command()
async def save(ctx, alias=None):
    """
    Alias and save the last rolled set of dice for a user.
    """
    if not alias:
        await ctx.channel.send("Alias for roll save?")

        while True:
            msg = await client.wait_for('message')
            if alias.author == ctx.author:
                alias = msg.content.strip()
                if " " in alias:  # Strip to account for accidental spacebar strokes
                    raise ValueError("No whitespace in alias allowed")

    discord_id = ctx.author.id
    nickname = ctx.author.nick
    save_user(db_curs, discord_id, nickname)


client.run(TOKEN)
