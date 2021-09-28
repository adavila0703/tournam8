import asyncio
from src.tests.future_creator import future_creator

class MessageMock:
    def __init__(self) -> None:
        pass

    def add_reaction(self, reaction):
        return future_creator(reaction)