from typing import Text
from discord.channel import TextChannel
from discord.guild import Guild
from discord import Member
from discord.reaction import Reaction
from src.bot.bot import BOT as bot
from discord import Message, User
from src.state.tournament_state import TOURNAMENT_STATE as tournament_state
from src.utils.output_message import OUTPUTS
from discord import RawReactionActionEvent, CategoryChannel


@bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    if user == bot.user:
        return None
    
    category_split: Message = reaction.message.channel.category.name.split('_')
    tournament_id = category_split[len(category_split) - 1]
    
    # TODO: need to create a check to see if the message you are reacting to is owned by the bot
    if tournament := tournament_state.tournaments.get(tournament_id):
        tournament_state.player_signed_up(tournament_id, user.name)
        await user.send(OUTPUTS['SIGNUP_SUCCESS'] + tournament['name'] + ' Good Luck!')

@bot.event
async def on_raw_reaction_remove(payload: RawReactionActionEvent):
    user: User = await bot.fetch_user(payload.user_id)
    guild: Guild = bot.get_guild(payload.guild_id)
    channel: TextChannel = guild.get_channel(payload.channel_id)
    category: CategoryChannel = channel.category
    category_split = str(category.name).split('_')
    tournament_id = category_split[len(category_split) - 1]

    # TODO: need to create a check to see if the message you are reacting to is owned by the bot
    if tournament := tournament_state.tournaments.get(tournament_id):
        tournament_state.player_removed_from_signups(tournament_id, user.name)
        await user.send(OUTPUTS['REMOVED_SIGNUPS'] + tournament['name'])