from src.client.tournament_client import TOURNAMENT_CLIENT, TournamentClient

STATUS = {
    'CREATED': 'Player Added.',
    'CLEARED': 'Player list cleared.',
    'ERROR_STATUS_CODE': 'Status code did not return 200...'
}

class PlayerListState:
    """State which holds a current list of players who own a have a screenshot channel."""
    def __init__(self, tournament_client: TournamentClient) -> None:
        self.tournament_client = tournament_client     
        self.players = set(self.get_player_list())

    def add_player_to_list(self, player_name: str) -> STATUS:
        """Appends new player to SessionState player list and send data to /players endpoint"""
        response = self.tournament_client.send_data('/add_player', { 'player': player_name }, 'add_player')

        if response.status_code != 200:
            return STATUS['ERROR_STATUS_CODE']

        self.players.add(player_name)
        print('Client -> ', self.players)
        return STATUS['CREATED']
    
    def clear_player_list(self) -> STATUS:
        self.tournament_client.send_data('/clear_player_list', {}, 'clear_player_list')
        self.players.clear()
        return STATUS['CLEARED']

    def get_player_list(self) -> STATUS:
        response, content = self.tournament_client.get_data('/get_player_list')

        if response.status_code != 200:
            return STATUS['ERROR_STATUS_CODE']

        return content


# PLAYER_LIST = PlayerListState(TOURNAMENT_CLIENT)
