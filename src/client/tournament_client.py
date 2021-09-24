import json
import requests
from requests import Response
from dotenv import dotenv_values

ENV = dotenv_values('.env')

class TournamentClient:
    def __init__(self, requestor: requests = requests) -> None:
        self.path = f"http://{ ENV['HOST'] }:{ ENV['PORT'] }"
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
