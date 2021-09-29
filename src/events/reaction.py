from typing import Text
from discord.channel import TextChannel
from discord.guild import Guild
from discord.reaction import Reaction
from discord import Message, User
from src.state.tournament_state import TOURNAMENT_STATE
from src.utils.output_message import OUTPUTS
from discord import RawReactionActionEvent, CategoryChannel
from discord.ext import commands

class ReactionCoordinator(commands.Cog):
    def __init__(
        self,
        bot,
        tournament_state = TOURNAMENT_STATE
    ) -> None:
        self.bot = bot
        self.tournament_state = tournament_state

    @commands.Cog.listener()
    async def on_reaction_add(
        self,
        reaction: Reaction, 
        user: User
    ):
        if user == self.bot.user:
            return None
        
        category_split: Message = reaction.message.channel.category.name.split('_')
        tournament_id = category_split[len(category_split) - 1]
        
        # TODO Message reacting to is from the bot / tournament(on_reaction_add)
        # Need to create a check to see if the message you are reacting to is owned by the bot
        # and/or part of an existing tournament
        if tournament := self.tournament_state.tournaments.get(tournament_id):
            self.tournament_state.player_signed_up(tournament_id, user.name)
            await user.send(OUTPUTS['SIGNUP_SUCCESS'] + tournament['name'] + ' Good Luck!')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, 
        payload: RawReactionActionEvent
    ):
        user: User = await self.bot.fetch_user(payload.user_id)
        guild: Guild = self.bot.get_guild(payload.guild_id)
        channel: TextChannel = guild.get_channel(payload.channel_id)
        category: CategoryChannel = channel.category
        category_split = str(category.name).split('_')
        tournament_id = category_split[len(category_split) - 1]

        # TODO Message reacting to is from the bot / tournament (on_raw_reaction_remove)
        # Need to create a check to see if the message you are reacting to is owned by the bot
        # and/or part of an existing tournament
        if tournament := self.tournament_state.tournaments.get(tournament_id):
            self.tournament_state.player_removed_from_signups(tournament_id, user.name)
            await user.send(OUTPUTS['REMOVED_SIGNUPS'] + tournament['name'])