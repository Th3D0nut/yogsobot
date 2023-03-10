from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("GUILD_NAME")
ROOT = join(dirname(__file__), "..")
