import discord
from discord.ext import commands

from settings import TOKEN
from userinput.parse import parse_roll_expression
import dice

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has joined the server!")


# maybe implement later
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     await bot.process_commands(message)


@bot.command()
async def roll(ctx, *expressions):
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

    author = str(ctx.author).split("#")[0]
    result = sum(rolled_dice)
    response = f"{author} rolled some dice, added together we get: {result}"
    await ctx.channel.send(response)


bot.run(TOKEN)
