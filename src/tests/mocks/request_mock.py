import json

class RequestMock:
    def __init__(self) -> None:
        pass

    def post(self, *args, **krgs):
        return self

    def get(self, *args, **krgs):
        return self

    @property
    def status_code(self):
        return 200
    
    @property
    def content(self):
        return json.dumps({ 'data': 'test' })
