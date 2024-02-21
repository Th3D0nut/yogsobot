from settings import TOKEN, client


if __name__ == "__main__":
    if TOKEN is None:
        raise TypeError(
            "TOKEN cannot be None and has to be of string containing a discord token."
        )
    import commands
    import events
    client.run(TOKEN)

