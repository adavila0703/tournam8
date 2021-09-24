import asyncio
from discord.ext.commands import Context

class LoggerMock():
    def __init__(self) -> None:
        pass

    def message_to_channel(self, ctx: Context, message: str, incoming_channel: str):
        future = asyncio.Future()
        future.set_result(message)
        return future