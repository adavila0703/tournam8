
class PlayerListStateMock:
    def __init__(self) -> None:
        self.players = set()   

    def add_player_to_list(self, player_name: str) -> None:
        self.players.add(player_name)
    
    def clear_player_list(self) -> None:
        self.players.clear()
