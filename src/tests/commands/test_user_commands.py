from src.commands.user_commands import UserCommander
from unittest.mock import Mock
import pytest

bot_mock = Mock()
ctx_mock = Mock()
commander = UserCommander(bot_mock)

@pytest.mark.asyncio
async def test_get_stats():
    await commander.get_stats(ctx_mock)