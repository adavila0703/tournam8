from discord.ext.commands import Context
from discord.channel import CategoryChannel, TextChannel
from discord.guild import Guild
from discord import Message
from discord.reaction import Reaction

class BotCommands:
    """Private methods that should only be handled by the bot"""
    def __init__(self) -> None:
        pass

    async def _create_category(
        self,
        ctx: Context,
        category_name: str
    ) -> CategoryChannel:
        guild: Guild = ctx.guild
        category: CategoryChannel = await guild.create_category(category_name)
        return category

    async def _create_text_channel_category(
        self,
        ctx: Context,
        channel_name: str, 
        category: CategoryChannel
    ) -> TextChannel:
        guild: Guild = ctx.guild
        channel: TextChannel = await guild.create_text_channel(name=channel_name, category=category)
        return channel

    async def _send_message_to_channel(
        self,
        ctx: Context,
        message: str, 
        channel: TextChannel, 
        reaction: Reaction
    ):
        message: Message = await channel.send(message)
    #TODO: Should reactions be its own method???
        return await message.add_reaction(reaction)

    # TODO: maybe make reactions a list if you want multiple reactions
    async def _start_sign_ups(
        self,
        ctx: Context,
        category_name: str, 
        channel_name: str, 
        reaction: Reaction, 
        message: str,
    ):
        category: CategoryChannel = await self._create_category(ctx, category_name)
        channel: TextChannel = await self._create_text_channel_category(ctx, channel_name, category)
        reaction = await self._send_message_to_channel(message, channel, reaction)
        return { 
            'STATUS': 'start_up_completed',
            'category': category,
            'channel': channel,
            'reaction': reaction
        }
        
    




