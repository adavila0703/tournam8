from src.state.tournament_state import TOURNAMENT_STATE, TournamentState
from discord.ext.commands import Context
import src.utils.logger as Logger
from src.utils.reactions import REACTIONS
from discord.ext import commands
from src.utils.string_type import STRING_TYPE

class TournamentCommander(commands.Cog):
    def __init__(
        self, 
        bot,
        tournament_state: TournamentState = TOURNAMENT_STATE,
        logger: Logger = Logger
    ) -> None:
        self.bot = bot
        self.tournament_state = tournament_state
        self.logger = logger

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_tournament(
        self,
        ctx: Context,
        name: str
    ) -> Context.send:
        """Creates a tournament"""
        status = self.tournament_state.create_tournament(name)
        await self.logger.message_to_channel(ctx, status, None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def start_signups(
        self,
        ctx: Context, 
        id,
    ) -> Context.send:
        status = await self.tournament_state.start_signups(ctx, id, REACTIONS[':check_mark_button:'])
        await self.logger.message_to_channel(ctx, status, None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete_tournament(
        self,
        ctx: Context, 
        uuid: str
    ) -> Context.send:
        status = self.tournament_state.delete_tournament(uuid)
        await self.logger.message_to_channel(ctx, status, None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def start_tournament(
        self,
        ctx: Context,
        uuid: str
    ) -> Context.send:
        status = self.tournament_state.start_tournament(uuid)
        await self.logger.message_to_channel(ctx, status, None)


    # TODO: tournaments[id] and tournaments['id'] can be confusing
    @commands.command()
    async def show_tournament_list(
        self,
        ctx: Context
    ) -> Context.send:
        tournaments = self.tournament_state.show_tournament_list()
        for index, id in enumerate(tournaments):
            tournament = tournaments[id]
            await self.logger.message_to_channel(ctx, self.string_constructor(index + 1, tournament, STRING_TYPE['LIST']), None)
        return tournaments

    @commands.command()
    async def show_tournament_details(
        self,
        ctx: Context, 
        uuid: str
    ) -> Context.send:
        tournament = self.tournament_state.show_tournament(uuid)
        await self.logger.message_to_channel(ctx, self.string_constructor(None, tournament, STRING_TYPE['SINGLE']), None)
        return tournament

    
    def string_constructor(
        self,
        index: int, 
        tournament: dict, 
        type
    ) -> str:
        status = 'Started' if tournament['status'] == True else 'Not Started'
        
        if type == STRING_TYPE['LIST']:
            return f"{index}. Tournament Id: {tournament['id']}\
            \nName: {tournament['name']}\
            \nStatus: {status}"

        elif type == STRING_TYPE['SINGLE']:
            return f"Tournament Id: {tournament['id']}\
            \nName: {tournament['name']}\
            \nStatus: {status}\
            \nPlayers Signed Up: {tournament['players_signed_up']}\
            \nPlayers Attended: {tournament['players_attended']}"