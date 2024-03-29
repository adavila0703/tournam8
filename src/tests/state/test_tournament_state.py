from asyncio import Future
from src.tests.future_creator import future_creator
from unittest.mock import Mock
import pytest
from src.state.tournament_state import TournamentState
from src.utils.status import TournamentStatus


uuid = Mock()
client_happy = Mock()
client_sad = Mock()
good_status = Mock()
bad_status = Mock()
ctx_mock = Mock()
start_up_mock = Mock()

start_up_mock.return_value = future_creator('')

good_status.status_code = 200
bad_status.status_code = 400

client_happy.send_data.return_value = good_status
client_sad.send_data.return_value = bad_status

client_happy.get_data.return_value = good_status, { 'id': { 'id': '123-222', 'name': 'test' } }
client_sad.get_data.return_value = bad_status, ''

uuid.uuid4.return_value = '123-321'

tournament_state_happy = TournamentState(client_happy, uuid, start_up_mock)
tournament_state_sad = TournamentState(client_sad, uuid, start_up_mock)

@pytest.fixture(autouse=True)
def pytest_reset_mocks():
    client_happy.reset_mock()
    client_sad.reset_mock()
    uuid.reset_mock()
    good_status.reset_mock()
    bad_status.reset_mock()
    ctx_mock.reset_mock()

def test_create_tournament():
    happy = tournament_state_happy.create_tournament('name')
    assert happy == {
        TournamentStatus.TOURNAMENT_CREATED: {
            'id': '123-321', 
            'name': 'name', 
            'status': False, 
            'players_signed_up': [], 
            'players_attended': [], 
            'player_stats': {}, 
            'channel_name': 'name_123-321'
            }
        }
    client_happy.send_data.assert_called_with('/create_tournament', happy[TournamentStatus.TOURNAMENT_CREATED], 'create_tournament')

    sad = tournament_state_sad.create_tournament('name')
    assert sad == TournamentStatus.ERROR_STATUS_CODE

# writing this realizing we weren't doing a check if the id exists
def test_delete_tournament():
    happy = tournament_state_happy.delete_tournament('id')
    assert happy == { TournamentStatus.TOURNAMENT_DELETED: 'id' }
    # TODO: Assertion error in test
    # labels: Tests
    # client_happy.send_data.assert_called_with('/create_tournament', { 'id': 'id' }, 'create_tournament')

    sad = tournament_state_sad.delete_tournament('id')
    assert sad == TournamentStatus.ERROR_STATUS_CODE

def test_get_all_tournaments():
    happy = tournament_state_happy.get_all_tournaments()
    assert happy == {
        '123-321': {
            'id': '123-321', 
            'name': 'name', 
            'status': False, 
            'players_signed_up': [], 
            'players_attended': [], 
            'player_stats': {}, 
            'channel_name': 
            'name_123-321'
        }
    }
    client_happy.get_data.assert_called_with('/get_all_tournaments')

    sad = tournament_state_sad.get_all_tournaments()
    assert sad == {}

def test_show_tournament_list():
    happy = tournament_state_happy.show_tournament_list()
    assert happy == {
        '123-321': {
            'id': '123-321', 
            'name': 'name', 
            'status': False, 
            'players_signed_up': [], 
            'players_attended': [], 
            'player_stats': {}, 
            'channel_name': 
            'name_123-321'
        }
    }

def test_show_tournament():
    happy = tournament_state_happy.show_tournament('123-321')
    assert happy == {
        'id': '123-321', 
        'name': 'name', 
        'status': False, 
        'players_signed_up': [], 
        'players_attended': [], 
        'player_stats': {}, 
        'channel_name': 
        'name_123-321'
    }

@pytest.mark.asyncio
async def test_start_signups():
    status = await tournament_state_happy.start_signups(ctx_mock, '123-321', 'rection')
    assert status == TournamentStatus.SIGNUPS_STARTED

def test_start_tournament():
    happy = tournament_state_happy.start_tournament('123-321')
    assert happy == TournamentStatus.TOURNAMENT_STARTED

    sad = tournament_state_sad.start_tournament('123-321')
    assert sad == TournamentStatus.TOURNAMENT_NOT_FOUND

def test_player_signed_up():
    happy = tournament_state_happy.player_signed_up('123-321', 'player')
    assert happy == TournamentStatus.PLAYER_SIGNED_UP

    sad = tournament_state_sad.player_signed_up('123-321', 'player')
    assert sad == TournamentStatus.ERROR_STATUS_CODE

# TODO: Tournament state reset
# labels: Tests
# State is retaining during this test, implement a way to reset the state after each test.
def test_valid_tournament_player():
    print(tournament_state_happy.tournaments)
    check_all = tournament_state_happy.valid_tournament_player('123-321', 'player')
    check_player = tournament_state_happy.valid_tournament_player('123-321', 'other_player')

    tournament_state_happy.tournaments['123-321']['status'] = False
    check_status = tournament_state_happy.valid_tournament_player('123-321', 'player')
    tournament_state_happy.tournaments['123-321']['status'] = True

    check_tournament = tournament_state_happy.valid_tournament_player('1', 'player')

    assert check_all == True
    assert check_player == False
    assert check_status == False
    assert check_tournament == False

def test_record_player_stats():
    happy = tournament_state_happy.record_player_stats('123-321', 'player', [1, 2, 3])
    assert happy == {'player': {'1': [1, 2, 3]}}

    sad = tournament_state_sad.record_player_stats('123-321', 'player', [1, 2, 3])
    assert sad == TournamentStatus.ERROR_STATUS_CODE
