from src.utils.string_type import StringType
from discord.ext.commands.core import command
import pytest
from src.commands.tournament_commands import TournamentCommander
from unittest.mock import Mock
from src.tests.future_creator import future_creator

ctx_mock = Mock()
tournament_state_mock = Mock()
logger_mock = Mock()
bot_mock = Mock()

test_tournament = 'test_tournament'
uuid_mock = '123'
future = future_creator(test_tournament)

logger_mock.message_to_channel.return_value = future
commander = TournamentCommander(bot_mock, tournament_state_mock, logger_mock)

@pytest.mark.asyncio
async def test_create_tournament():
    tournament_state_mock.create_tournament.return_value = future
    await commander.create_tournament(commander, ctx_mock, test_tournament)
    logger_mock.message_to_channel.assert_called_with(ctx_mock, future, None)

@pytest.mark.asyncio
async def test_delete_trounament():
    tournament_state_mock.delete_tournament.return_value = future
    await commander.delete_tournament(commander, ctx_mock, uuid_mock)
    logger_mock.message_to_channel.assert_called_with(ctx_mock, future, None)

@pytest.mark.asyncio
async def test_start_tournament():
    tournament_state_mock.start_tournament.return_value = future
    await commander.start_tournament(commander, ctx_mock, uuid_mock)
    logger_mock.message_to_channel.assert_called_with(ctx_mock, future, None)

@pytest.mark.asyncio
async def test_show_tournament_list():
    data = { 
        'id': { 'id': 1, 'name': 'test_list', 'status': False, 'players_signed_up': [], 'players_attended': [] },
        'id': { 'id': 2, 'name': 'test_list', 'status': False, 'players_signed_up': [], 'players_attended': [] } 
    }
    tournament_state_mock.show_tournament_list.return_value = data
    tournaments = await commander.show_tournament_list(commander, ctx_mock)
    assert tournaments == data

@pytest.mark.asyncio
async def test_show_tournament_details():
    data = {'id': 1, 'name': 'test_list', 'status': False, 'players_signed_up': [], 'players_attended': []}
    tournament_state_mock.show_tournament.return_value = data
    tournament = await commander.show_tournament_details(commander, ctx_mock, '123')
    tournament_state_mock.show_tournament.assert_called_with(uuid_mock)
    logger_mock.message_to_channel.assert_called_with(ctx_mock, commander.string_constructor(None, data, StringType.SINGLE), None)
    assert tournament == data

@pytest.mark.asyncio
async def test_start_signups():
    tournament_state_mock.start_signups.return_value = future
    await commander.start_signups(commander, ctx_mock, uuid_mock)
    logger_mock.message_to_channel.assert_called_with(ctx_mock, test_tournament, None)

