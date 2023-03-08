import discord
from discord.ext import commands

from settings import TOKEN
from userinput.parse import parse_roll_expression
import dice

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

roll_history = {}  # roll function fills this


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
async def r(ctx, *expressions):  # roll, keep short for easier command
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

    roll_history[str(ctx.author)] = expressions


async def save(ctx, alias):
    """
    Alias and save the last rolled set of dice for a user.
    """
    pass


bot.run(TOKEN)
