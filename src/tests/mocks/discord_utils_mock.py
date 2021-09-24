import asyncio

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
            future = asyncio.Future()
            future.set_result('good')
            self.channels.clear()
            return future