from asyncio import Future

def future_creator(result):
    future = Future()
    future.set_result(result)
    return future