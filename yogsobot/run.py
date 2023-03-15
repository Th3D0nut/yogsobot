import sqlite3
from os.path import join

import discord
from discord.ext import commands

from settings import TOKEN, ROOT, MY_ID 
from userinput.parse import parse_roll_expression
from database.utills import init_tables
import dice

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

roll_history = []  # Roll function fills this

PATH_TO_DB = join(ROOT, "aliasroll.db")
db_connection = sqlite3.connect(PATH_TO_DB)
db_curs = db_connection.cursor()
init_tables(db_curs)


@bot.event
async def on_ready():
    print(f"{bot.user} has joined the server!")


@bot.command()
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


@bot.command()
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
    response = f"{ctx.author.nick} rolled some dice, added together we get: {result}"
    await ctx.channel.send(response)

    roll_history.append({
            "id": ctx.author.id,
            "nickname": ctx.author.nick,
            "expression": expressions,
        })


@bot.command()
async def shutdown(ctx):
    """Remote shutdown"""
    if ctx.author.id == MY_ID:
        await bot.close()


# @bot.command()
# async def save(ctx):
#     """
#     Alias and save the last rolled set of dice for a user.
#     """
#     discord_id = ctx.author.id
#     nick = ctx.author.nick
#     user = db_curs.execute(
#         "SELECT discord_id FROM user WHERE discord_id = ?;",
#         discord_id
#         )
#     if not user.fetchone():
#         db_curs.execute(
#             "INSERT INTO user (discord_id, nick) VALUES (?, ?);",
#             discord_id, nick
#             )


bot.run(TOKEN)
