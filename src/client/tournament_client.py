import json
import requests
from requests import Response
from src.env.env import ENV

class TournamentClient:
    def __init__(self, requestor: requests = requests) -> None:
        self.path = f"{ ENV['API_PATH'] }"
        self.http_request = requestor

    def get_data(self, endpoint: str) -> Response.content:
        response = self.http_request.get(self.path + endpoint)
        content = json.loads(response.content)
        return response, content

    def send_data(self, endpoint: str, body: dict, type: str) -> Response:
        json_body = json.dumps(body)
        response = self.http_request.post(self.path + endpoint, json_body)
        print(f'Request Type: { type }, Status Code: { response.status_code }')
        return response

TOURNAMENT_CLIENT = TournamentClient()
