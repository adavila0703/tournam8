import asyncio
from discord.ext.commands import Context
from src.tests.future_creator import future_creator

class LoggerMock():
    def __init__(self) -> None:
        pass

    def message_to_channel(self, ctx: Context, message: str, incoming_channel: str):
        return future_creator(message)