import uuid
from dataclasses import dataclass, asdict
from discord.ext.commands import Context
from discord.reaction import Reaction
from src.client.tournament_client import TOURNAMENT_CLIENT as tournament_client, TournamentClient
from src.bot.bot_commands import BotCommands
from src.utils.output_message import OUTPUTS
from src.utils.status import TOURNAMENT_STATUS as STATUS

class TournamentState:
    """Holds state of all created tournaments"""
    def __init__(self, client: TournamentClient, uuid: uuid, start_signup_command) -> None:
        self.client = client
        self.uuid = uuid
        self.start_signup_command = start_signup_command
        self.tournaments = self.get_all_tournaments()

    @dataclass
    class Tournament():
        """Data class for a single tournament"""
        id: uuid
        name: str
        status: bool
        players_signed_up: list
        players_attended: list
        player_stats: dict
        channel_name: str

    def get_all_tournaments(self):
        """Reaches out to the api to get all active tournaments"""
        # TODO Possible failing test for get_all_tournaments
        # labels: state, tests
        # Destructuring get_data() return was causing error on test.
        response, content = self.client.get_data('/get_all_tournaments')

        if response.status_code != 200:
            return STATUS['ERROR_STATUS_CODE']

        return content

    def create_tournament(
        self, 
        name: str
    ) -> dict:
        """Creates a tournament"""
        id = str(self.uuid.uuid4())
        tournament = self.Tournament(id, name, False, [], [], {}, name + '_' + id)
        as_dict = asdict(tournament)
        response = self.client.send_data('/create_tournament', as_dict, 'create_tournament')
        print(response.status_code)
        if response.status_code != 200:
            return STATUS['ERROR_STATUS_CODE']

        self.tournaments[tournament.id] = as_dict
        # print('Client -> ', self.tournaments)
        return { STATUS['TOURNAMENT_CREATED']: as_dict }

    def delete_tournament(
        self, 
        id: str
    ) -> dict:
        """Deletes a tournament"""
        response = self.client.send_data('/delete_tournament', { 'id': id }, 'delete_tournament')

        if response.status_code != 200:
            return STATUS['ERROR_STATUS_CODE']
        
        if self.tournaments.get(id):
            self.tournaments.pop(id)

        return { STATUS['TOURNAMENT_DELETED']: id }

    def show_tournament_list(self):
        """Shows a list of created tournaments"""
        return self.tournaments

    def show_tournament(self, id):
        """Shows details of a current tournament"""
        return self.tournaments[id]

    async def start_signups(self, ctx: Context, id: int, reaction: Reaction):
        """Begins the signup phase for your tournament"""

        # TODO Category and channel check
        # labels: state
        # Do a check if the category and channel have already been created.
        await self.start_signup_command(ctx, self.tournaments[id]['channel_name'], f'General - {id}', reaction, OUTPUTS['SIGNUP'])
        return STATUS['SIGNUPS_STARTED']

    def start_tournament(self, id: str) -> STATUS:
        """Sets tournament stats to True and sets the signed up players to the active list"""
        # TODO Create method to check of if tournament exists
        # labels: quick, state, duplicate
        # This is code duplication, create a method for this
        if (tournament := self.tournaments.get(id)) == None:
            return STATUS['TOURNAMENT_NOT_FOUND']

        if tournament['status'] == False:
            response = self.client.send_data('/start_tournament', { 'id': tournament['id'], 'tournament': tournament }, 'start_tournament')
            
            if response.status_code != 200:
                return STATUS['ERROR_STATUS_CODE']

            tournament['status'] = True
            tournament['players_attended'] = tournament['players_signed_up']
 
        return STATUS['TOURNAMENT_STARTED']

    def player_signed_up(self, id, player):
        """Stores the player who just signed up in state and sends data to API"""
        response = self.client.send_data('/player_signed_up', { 'id': id, 'player': player }, 'player_signed_up')

        if response == 200:
            return STATUS['ERROR_STATUS_CODE']

        self.tournaments[id]['players_signed_up'].append(player)
        print('Client -> ', self.tournaments)
        return STATUS['PLAYER_SIGNED_UP']

    def player_removed_from_signups(self, id, player):
        """Removes player from signups"""
        response = self.client.send_data('/player_removed_from_signups', { 'id': id, 'player': player }, 'player_removed_from_signups')
        player_list = self.tournaments[id]['players_signed_up']

        if response == 200:
            return STATUS['ERROR_STATUS_CODE']

        if player in player_list:
            player_list.remove(player)
        print('Client -> ', self.tournaments)
        return STATUS['PLAYER_SIGNED_UP']

    def valid_tournament_player(self, id: str, player: str) -> bool:
        """Checks if the incoming tournment exists, is active and the player is also active"""
        if (tournament := self.tournaments.get(id)) == None:
            return False
        if tournament['status'] == False:
            return False
        if player not in tournament['players_attended']:
            return False
        
        return True

    def record_player_stats(self, id: str, player: str, stats: dict):
        response, content = self.client.get_data('/')

        if response.status_code != 200:
            return STATUS['ERROR_STATUS_CODE']

        if (tournament := self.tournaments.get(id)) == None:
            return STATUS['TOURNAMENT_NOT_FOUND']

        self.client.send_data('/record_player_stats', { 'id': id, 'stats': stats, 'player': player }, 'record_player_stats')
            
        player_stats = tournament['player_stats']

        if not player_stats.get(player):
            player_stats[player] = { '1': stats }
        else:
            player_stats[player][str(len(player_stats[player]) + 1)] = stats

        return player_stats

bot_commands = BotCommands()
TOURNAMENT_STATE = TournamentState(tournament_client, uuid, bot_commands._start_sign_ups)
