import asyncio
from src.tests.mocks.message_mock import MessageMock

class TextChannelMock:
    def __init__(self, name) -> None:
        self.message = MessageMock()
        self.name = name
    
    def __repr__(self) -> str:
        return self.name

    def send(self, message):
        future = asyncio.Future()
        future.set_result(self.message)
        return future