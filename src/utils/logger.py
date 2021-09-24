from discord import File
from discord.ext.commands import Context
import discord.utils


# TODO: Possible code duplication in bot_commands, check if this can be replaced
async def message_to_channel(ctx: Context, message: str, incoming_channel: str) -> None:
    """Directs a message out to a specific channel. Use None as channel to reply where the command was submitted"""
    if incoming_channel != None:
        channel = discord.utils.get(ctx.guild.text_channels, name=incoming_channel)
        await channel.send(message)
    await ctx.send(message)

async def file_to_channel(ctx: Context, channel: str, file: File) -> None:
    """Directs a file out to a specific channel. Use None as channel to reply where the command was submitted"""
    if channel != None:
        channel = discord.utils.get(ctx.guild.text_channels, name=channel)
        await channel.send(file=file)
    await ctx.send(file=file)

