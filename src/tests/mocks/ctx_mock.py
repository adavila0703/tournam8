import asyncio
from src.tests.mocks.text_channel_mock import TextChannelMock
from discord.channel import TextChannel
from src.tests.future_creator import future_creator

class CtxMock:
    def __init__(self) -> None:
        self.guild_mock = self.GuildMock()

    async def send(self, str: str):
        await future_creator(str)

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
            return future_creator(category_name)
        
        def create_text_channel(self, name: str, category: str):
            channel = TextChannelMock(name)
            self.categories[category] = channel
            return future_creator(channel)

        def voice_channels():
            return ''