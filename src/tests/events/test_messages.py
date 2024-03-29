from src.events.messages import MessageCoordinator
from unittest.mock import Mock
import pytest
from src.tests.future_creator import future_creator
from src.utils.status import MessageStatus

# TODO Mocks require cleanup
# labels: tests
# clean up mocks, maybe find a better way to create mocks?

bot_mock = Mock()
message_mock = Mock()
state_mock = Mock()
channel_mock = Mock()
logger_mock = Mock()
ocr = Mock()

logger_mock.message_to_channel.return_value = future_creator(None)
state_mock.valid_tournament_player.return_value = True
bot_mock.user = 'bot'
bot_mock.process_commands.return_value = future_creator(None)
message_mock.author = 'TestUser#1'

coordinator = MessageCoordinator(bot_mock, state_mock, logger_mock, ocr)

@pytest.fixture(autouse=True)
def pytest_reset_mocks():
    bot_mock.reset_mock() 
    message_mock.reset_mock() 
    state_mock.reset_mock()

@pytest.mark.asyncio
async def test_on_message_bot_message():
    "Tests if the incoming message is equal to a bot"
    message_mock.author = 'bot'
    result = await coordinator.on_message(message_mock)
    assert result == MessageStatus.BOT_MESSAGE

@pytest.mark.asyncio
async def test_on_message_no_attachments():
    "Tests if the incoming message.attachments is equal to an empty list"
    message_mock.attachments = []
    message_mock.author = 'TestUser#1'
    result = await coordinator.on_message(message_mock)
    assert result == MessageStatus.NO_ATTACHMENTS

@pytest.mark.asyncio
async def test_on_message_valid_tournament():
    "Tests if the incoming message.attachments is equal to an empty list"
    state_mock.valid_tournament_player.return_value = False
    message_mock.author = 'TestUser#1'
    channel_mock.category = "TestCategory_1"
    message_mock.channel = channel_mock
    message_mock.attachments = [
        'test'
    ]
    result = await coordinator.on_message(message_mock)
    assert result == MessageStatus.TOURNAMENT_OR_PLAYER_NOT_VALID

@pytest.mark.asyncio
async def test_on_message_success():
    "Tests if the incoming message.attachments is equal to an empty list"
    state_mock.valid_tournament_player.return_value = True
    message_mock.author = 'TestUser#1'
    message_mock.save.return_value = future_creator(None)
    channel_mock.category = "TestCategory_1"
    channel_mock.send.return_value = future_creator(None)
    message_mock.channel = channel_mock
    message_mock.attachments = [
        message_mock
    ]
    result = await coordinator.on_message(message_mock)
    assert result == MessageStatus.PLAYER_STATS_RECORDED

