import asyncio
class TournamentStateMock:
    def __init__(self) -> None:
        self.tournaments = []
        self.tournament_start = False
        self.tournment_list = { 
            '1': {'id': 1, 'name': 'test_list', 'status': False}, 
            '2': {'id': 2, 'name': 'test_list', 'status': False},
            '3': {'id': 3, 'name': 'test_list', 'status': False, 'players_signed_up': [], 'players_attended': []}, 
        }
        self.signups = False

    def create_tournament(self, name):
        self.tournaments.append(name)
        return 'Completed'

    def delete_tournament(self, id):
        self.tournaments.pop(0)
        return 'Completed'
        
    def start_tournament(self, id):
        self.tournament_start = True
        return 'Completed'

    def show_tournament_list(self):
        return self.tournment_list

    def show_tournament(self, id):
        return self.tournment_list[id]

    def start_signups(self, ctx, id, reactions):
        self.signups = True
        future = asyncio.Future()
        future.set_result('completed')
        return future