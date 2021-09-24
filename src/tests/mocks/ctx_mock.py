import asyncio
from src.tests.mocks.text_channel_mock import TextChannelMock
from discord.channel import TextChannel

class CtxMock:
    def __init__(self) -> None:
        self.guild_mock = self.GuildMock()

    async def send(self, str: str):
        future = asyncio.Future()
        future.set_result(str)
        await future

    @property
    def guild(self):
        return self.guild_mock

    class GuildMock:
        def __init__(self) -> None:
            self.categories = {}

        @property
        def text_channels(self):
            pass

        def create_category(self, category_name):
            self.categories[category_name] = ''
            future = asyncio.Future()
            future.set_result(category_name)
            return future
        
        # TODO: set result to categories not incoming string aname
        def create_text_channel(self, name: str, category: str):
            channel = TextChannelMock(name)
            self.categories[category] = channel
            future = asyncio.Future()
            future.set_result(channel)
            return future

        def voice_channels():
            return ''