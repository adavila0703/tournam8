
from discord import Message
from src.ocr.ocr import ocr
import os
from src.state.tournament_state import TOURNAMENT_STATE, TournamentState
from discord.ext import commands
from src.utils.status import MESSAGE_STATUS as STATUS

class MessageCoordinator(commands.Cog):
    def __init__(
        self,
        bot,
        tournament_state: TournamentState = TOURNAMENT_STATE
    ) -> None:
        self.bot = bot
        self.tournament_state = tournament_state

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Event which handles reading the screenshot information"""
        if message.author == self.bot.user:
            return STATUS['BOT_MESSAGE']

        await self.bot.process_commands(message)

        if message.attachments == []:
            return STATUS['NO_ATTACHMENTS']

        channel = message.channel

        user = str(message.author).split('#')[0]
        category = str(message.channel.category).split('_')
        tournament_id = category[len(category) - 1]

        if not self.tournament_state.valid_tournament_player(tournament_id, user):
            return STATUS['TOURNAMENT_OR_PLAYER_NOT_VALID']
        
        path = './' + user + '.png'

        with open(path, 'w') as file:
        # TODO Check for PNG
        # This is currently not checking if the incoming image is a PNG


        # TODO In memory image instead of disk
        # Instead of saving the image to the disk, we could keep it in memory using numpy
            await message.attachments[0].save(path)
            stats = ocr(path)
            file.close()
            os.remove(path)
        
        self.tournament_state.record_player_stats(tournament_id, user, stats)
        await channel.send(f'User: {user} Game Stats: {stats}')
        return STATUS['PLAYER_STATS_RECORDED']
