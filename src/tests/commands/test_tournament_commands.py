from src.tests.future_creator import future_creator
import pytest
from src.commands.tournament_commands import TournamentCommander
from unittest.mock import Mock


ctx_mock = Mock()
tournament_state_mock = Mock()
logger_mock = Mock()
bot_mock = Mock()

tournament_state_mock.create_tournament.return_value = future_creator('test_tournament')

commander = TournamentCommander(bot_mock, tournament_state_mock, logger_mock)

#TODO: Major refactor required / Broken tests
# labels: Tests
# Refactor this file to accept unittest.mock 

# @pytest.mark.asyncio
# async def test_create_tournament():
#     woop = TournamentCommander(bot_mock, tournament_state_mock, logger_mock)
#     status = await woop.create_tournament(ctx_mock, 'test_tournament')
#     print(status)
#     assert 3 == 2

# @pytest.mark.asyncio
# async def test_delete_trounament():
#     await commander.delete_tournament(ctx_mock, '123')
#     # assert tournament_state.tournaments == []

# @pytest.mark.asyncio
# async def test_start_tournament():
#     await commander.start_tournament(ctx_mock, '123')
#     # assert tournament_state.tournament_start == True

# @pytest.mark.asyncio
# async def test_show_tournament_list():
#     tournaments = await commander.show_tournament_list(ctx_mock)
#     assert tournaments == { 
#             '1': {'id': 1, 'name': 'test_list', 'status': False}, 
#             '2': {'id': 2, 'name': 'test_list', 'status': False},
#             '3': {'id': 3, 'name': 'test_list', 'status': False, 'players_signed_up': [], 'players_attended': []}, 
#         }
# @pytest.mark.asyncio
# async def test_show_tournament_details():
#     tournaments = await commander.show_tournament_details(ctx_mock, '3')
#     assert tournaments == {'id': 3, 'name': 'test_list', 'status': False, 'players_signed_up': [], 'players_attended': []}

# @pytest.mark.asyncio
# async def test_start_signups():
#     await commander.start_signups(ctx_mock, '3')
#     # assert tournament_state.signups == True

