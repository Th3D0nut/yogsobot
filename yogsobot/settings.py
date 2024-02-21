from os import getenv, path
from os.path import join, dirname
from dotenv import load_dotenv

from discord import Intents
from discord.ext import commands


intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("GUILD_NAME")
MY_ID = getenv("DISCORD_ID")
ROOT = join(dirname(__file__), "..")
PATH_TO_DB = path.join(ROOT, "aliasroll.db")
