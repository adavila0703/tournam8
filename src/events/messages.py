
from discord import Message
from src.ocr.ocr import ocr
import os
from src.state.tournament_state import TOURNAMENT_STATE, TournamentState
from discord.ext import commands
from src.utils.status import MessageStatus
from src.utils import logger

class MessageCoordinator(commands.Cog):
    def __init__(
        self,
        bot,
        tournament_state: TournamentState = TOURNAMENT_STATE,
        log: logger = logger,
        ocr = ocr
    ) -> None:
        self.bot = bot
        self.tournament_state = tournament_state
        self.logger = log
        self.ocr = ocr

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Event which handles reading the screenshot information"""
        if message.author == self.bot.user:
            return MessageStatus.BOT_MESSAGE

        if message.attachments == []:
            status = MessageStatus.NO_ATTACHMENTS
            print(status)
            return status

        channel = message.channel

        user = str(message.author).split('#')[0]
        category = str(channel.category).split('_')
        tournament_id = category[len(category) - 1]

        if not self.tournament_state.valid_tournament_player(tournament_id, user):
            status = MessageStatus.TOURNAMENT_OR_PLAYER_NOT_VALID
            print(status)
            return status
        
        path = './' + user + '.png'

        with open(path, 'w') as file:
        # TODO Check for PNG
        # This is currently not checking if the incoming image is a PNG


        # TODO In memory image instead of disk
        # Instead of saving the image to the disk, we could keep it in memory using numpy
            await message.attachments[0].save(path)
            stats = self.ocr(path)
            file.close()
            os.remove(path)
        
        self.tournament_state.record_player_stats(tournament_id, user, stats)
        await channel.send(f'User: {user} Game Stats: {stats}')
        status = MessageStatus.PLAYER_STATS_RECORDED
        print(status)
        return status