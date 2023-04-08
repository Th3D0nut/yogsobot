import pytest

from yogsobot.run import roll, save
from database.test_transactions import db


roll_history = {}  # wanted side effect of roll


class ContextMock:
    def __init__(self) -> None:
        self.channel = ChannelMock()
        self.author = AuthorMock()
        

class AuthorMock:
    def __init__(self) -> None:
        self.display_name = "Jerek"
        self.id = "123456789"


class ChannelMock:
    def __init__(self) -> None:
        self.recieved = None

    async def send(self, msg):
        self.recieved = msg


@pytest.mark.asyncio
async def test_bad_roll_give_error_message_and_leaves_rest_empty():
    ctx = ContextMock()
    await roll(ctx, "lala")  # type: ignore
    assert str(ctx.channel.recieved) == "Must be of form <amount>d<side_amount>."  # type: ignore
