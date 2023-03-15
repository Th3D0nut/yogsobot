from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("GUILD_NAME")
MY_ID = getenv("ROAN_DISCORD_ID")
ROOT = join(dirname(__file__), "..")
