from discord import File
from discord.ext.commands import Context
import discord.utils


# TODO: Code duplication
# labels: duplication
# Go to src.bot.bot_commands has a similar method, do we want to keep both?
async def message_to_channel(ctx: Context, message: str, incoming_channel: str) -> None:
    """Directs a message out to a specific channel. Use None as channel to reply where the command was submitted"""
    # TODO Improvment needed for message_to_channel()
    # Possible code duplication but also this method can be changed.
    # You dont need to use discord.utils.get to get incoming text channel
    # Also what if we cannot get the incoming Context? Maybe generalize this method to accept incoming
    # channel name and then output to discord and stdout
    if incoming_channel != None:
        channel = discord.utils.get(ctx.guild.text_channels, name=incoming_channel)
        print(message)
        await channel.send(message)
    print(message)
    await ctx.send(message)

async def file_to_channel(ctx: Context, channel: str, file: File) -> None:
    """Directs a file out to a specific channel. Use None as channel to reply where the command was submitted"""
    if channel != None:
        channel = discord.utils.get(ctx.guild.text_channels, name=channel)
        await channel.send(file=file)
    await ctx.send(file=file)

