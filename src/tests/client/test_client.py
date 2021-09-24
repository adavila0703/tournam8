from src.client.tournament_client import TournamentClient
from src.tests.mocks.request_mock import RequestMock

requests = RequestMock()
client = TournamentClient(requests)

def test_get_data():
    response, content = client.get_data('/endpoint')
    assert(response.status_code == 200)
    assert(content == { 'data': 'test' })

def test_send_data():
    response = client.send_data('/endpoint', { 'body': 'data' }, 'atype')
    assert response.status_code == 200