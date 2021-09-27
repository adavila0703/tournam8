import asyncio
from src.tests.future_creator import future_creator

class DiscordUtilsMock:
    def __init__(self) -> None:
        self.channel_mock = self.ChannelMock()

    def get(self, channel, name):
        return self.channel_mock

    class ChannelMock:
        def __init__(self) -> None:
            self.channels = ['mock_channel']
            self.members = ['player1', 'player2']

        def delete(self):
            self.channels.clear()
            return future_creator('good')