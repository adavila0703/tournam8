from discord import message
from discord.ext.commands.errors import BotMissingAnyRole
from src.events.messages import MessageCoordinator
from unittest.mock import Mock
import pytest
from src.tests.future_creator import future_creator
from src.utils.status import MESSAGE_STATUS as STATUS

bot_mock = Mock()
message_mock = Mock()
state_mock = Mock()
state_mock.valid_tournament_player.return_value = True
coordinator = MessageCoordinator(bot_mock, state_mock)
bot_mock.user = 'bot'
message_mock.author = 'TestUser#1'
save_func = message_mock.save.return_value = future_creator(None)
message_mock.attachments == [
    save_func
]
message_mock.channel = "TestCategory_1"


@pytest.mark.asyncio
async def test_on_message_bot_message():
    "Tests if the incoming message is equal to a bot"
    message_mock.author = bot_mock.user
    result = coordinator.on_message(message_mock)
    assert result == STATUS['BOT_MESSAGE']

@pytest.mark.asyncio
async def test_on_message_no_attachments():
    "Tests if the incoming message.attachments is equal to an empty list"
    message_mock.attachments == []
    result = coordinator.on_message(message_mock)
    assert result == STATUS['NO_ATTACHMENTS']

@pytest.mark.asyncio
async def test_on_message_no_attachments():
    "Tests if the incoming message.attachments is equal to an empty list"
    state_mock.valid_tournament_player.return_value = False
    result = coordinator.on_message(message_mock)
    assert result == STATUS['TOURNAMENT_OR_PLAYER_NOT_VALID']

