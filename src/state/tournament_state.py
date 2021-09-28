import uuid
from dataclasses import dataclass, asdict
from discord.ext.commands import Context
from discord.reaction import Reaction
from src.client.tournament_client import TOURNAMENT_CLIENT as tournament_client, TournamentClient
from src.bot.bot_commands import BotCommands
from src.utils.output_message import OUTPUTS
from src.utils.status import TournamentStatus

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

    def get_all_tournaments(self, guild_id):
        """Reaches out to the api to get all active tournaments"""
        # TODO Possible failing test for get_all_tournaments
        # labels: state, tests
        # Destructuring get_data() return was causing error on test.
        response, content = self.client.get_data(
            '/get_all_tournaments', 
            { 'guild_id': guild_id }
        )

        if response.status_code != 200:
            return {}

        return content

    def create_tournament(
        self, 
        name: str,
        guild_id: int
    ) -> dict:
        """Creates a tournament"""
        tournament_id = str(self.uuid.uuid4())
        guild_id_str = str(guild_id)

        tournament = self.Tournament(tournament_id, name, False, [], [], {}, name + '_' + id)
        tournament_as_dict = asdict(tournament)

        response = self.client.send_data(
            '/create_tournament', 
            { 'guild_id': guild_id_str, 'data': tournament_as_dict }, 
            'create_tournament'
        )

        if response.status_code != 200:
            return TournamentStatus.ERROR_STATUS_CODE

        if guild := self.tournaments.get(guild_id_str):
            guild[guild_id_str].update({ tournament_id: tournament_as_dict })
        else:
            guild[guild_id_str] = { tournament_id: tournament_as_dict }
            

        print('Client -> ', self.tournaments)
        return { TournamentStatus.TOURNAMENT_CREATED: tournament_as_dict }

    def delete_tournament(
        self, 
        guild_id: int,
        tournament_id: str
    ) -> dict:
        """Deletes a tournament"""
        guild_id_str = str(guild_id)

        response = self.client.send_data(
            '/delete_tournament', 
            { 
                'guild_id': guild_id_str, 
                'tournament_id': tournament_id 
            }, 
            'delete_tournament'
        )

        if response.status_code != 200:
            return TournamentStatus.ERROR_STATUS_CODE
        
        if guild := self.tournaments.get(guild_id_str):
            if tournament := guild.get(tournament_id):
                tournament.pop(tournament_id)

        return { TournamentStatus.TOURNAMENT_DELETED: id }

    def show_tournament_list(self, guild_id):
        """Shows a list of created tournaments"""
        return self.tournaments[guild_id]

    def show_tournament(self, tournament_id, guild_id):
        """Shows details of a current tournament"""
        return self.tournaments[guild_id][tournament_id]

    async def start_signups(
        self, 
        ctx: Context,
        guild_id: int, 
        tournament_id: int, 
        reaction: Reaction
    ) -> TournamentStatus:
        """Begins the signup phase for your tournament"""

        # TODO Category and channel check
        # labels: state
        # Do a check if the category and channel have already been created.
        guild_id_str = str(guild_id)
        await self.start_signup_command(
            ctx, 
            self.tournaments[guild_id_str][tournament_id]['channel_name'], 
            f'General - {id}', 
            reaction, 
            OUTPUTS['SIGNUP']
        )
        return TournamentStatus.SIGNUPS_STARTED

    def start_tournament(
        self, 
        guild_id: int,
        tournament_id: str 
    ) -> TournamentStatus:
        """Sets tournament stats to True and sets the signed up players to the active list"""
        # TODO Create method to check of if tournament exists
        # labels: quick, state, duplicate
        # This is code duplication, create a method for this
        guild_id_str = str(guild_id)

        if (guild := self.tournaments.get(guild_id)) == None:
            return TournamentStatus.GUILD_NOT_FOUND

        if (tournament := guild.get(id)) == None:
            return TournamentStatus.TOURNAMENT_NOT_FOUND

        if tournament['status'] == False:
            response = self.client.send_data(
                '/start_tournament', 
                { 
                    'id': tournament['id'], 
                    'tournament': tournament 
                }, 
                'start_tournament'
            )
            
            if response.status_code != 200:
                return TournamentStatus.ERROR_STATUS_CODE

            tournament['status'] = True
            tournament['players_attended'] = tournament['players_signed_up']
 
        return TournamentStatus.TOURNAMENT_STARTED

    def player_signed_up(
        self,
        guild_id: int, 
        tournament_id: str, 
        player: str
    ) -> TournamentStatus:
        """Stores the player who just signed up in state and sends data to API"""
        guild_id_str = str(guild_id)
        response = self.client.send_data(
            '/player_signed_up', 
            { 
                'guild_id': guild_id_str,
                'tournament_id': tournament_id, 
                'player': player 
            }, 
            'player_signed_up'
        )

        if response.status_code != 200:
            return TournamentStatus.ERROR_STATUS_CODE

        # TODO Code Duplication on Guild/Tournament Check
        # Move this check to its own method, it is being used in other areas of the state
        self.
        if self.guil
            self.tournaments[guild_id][tournament_id]['players_signed_up'].append(player)

        print('Client -> ', self.tournaments)
        return TournamentStatus.PLAYER_SIGNED_UP

    def player_removed_from_signups(
        self,
        guild_id: int,
        tournament_id: str, 
        player
    ) -> TournamentStatus:
        """Removes player from signups"""
        guild_id_str = str(guild_id)

        response = self.client.send_data(
            '/player_removed_from_signups', 
            {
                'guild_id': guild_id_str,
                'tournament_id': tournament_id, 
                'player': player 
            }, 
            'player_removed_from_signups'
        )


        if response != 200:
            return TournamentStatus.ERROR_STATUS_CODE

        if not self.guild_tournament_check(guild_id_str, tournament_id):
            

            
        player_list = self.tournaments[guild_id_str][tournament_id]['players_signed_up']

        if player in player_list:
            player_list.remove(player)

        print('Client -> ', self.tournaments)
        return TournamentStatus.PLAYER_SIGNED_UP

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
            return TournamentStatus.ERROR_STATUS_CODE

        if (tournament := self.tournaments.get(id)) == None:
            return TournamentStatus.TOURNAMENT_NOT_FOUND

        self.client.send_data('/record_player_stats', { 'id': id, 'stats': stats, 'player': player }, 'record_player_stats')
            
        player_stats = tournament['player_stats']

        if not player_stats.get(player):
            player_stats[player] = { '1': stats }
        else:
            player_stats[player][str(len(player_stats[player]) + 1)] = stats
        return player_stats
    
    def guild_tournament_check(
        self,
        guild_id: str, 
        tournament_id: str
    ) -> bool:
        """Checks that the guild and tournment exists"""
        if guild := self.tournaments.get(guild_id):
            if guild.get(tournament_id):
                return True
        return False
                


bot_commands = BotCommands()
TOURNAMENT_STATE = TournamentState(tournament_client, uuid, bot_commands._start_sign_ups)
