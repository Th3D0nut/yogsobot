from settings import client


@client.event
async def on_ready():
    print(f"{client.user} has joined the server!")

