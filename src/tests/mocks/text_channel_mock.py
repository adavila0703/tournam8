import asyncio
from src.tests.mocks.message_mock import MessageMock
from src.tests.future_creator import future_creator

class TextChannelMock:
    def __init__(self, name) -> None:
        self.message = MessageMock()
        self.name = name
    
    def __repr__(self) -> str:
        return self.name

    def send(self, message):
        return future_creator(message)