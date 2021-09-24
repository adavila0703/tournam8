import asyncio

class MessageMock:
    def __init__(self) -> None:
        pass

    def add_reaction(self, reaction):
        future = asyncio.Future()
        future.set_result(reaction)
        return future