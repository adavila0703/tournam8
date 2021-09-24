from bot.bot import bot
import discord.utils
from discord.ext.commands import CommandNotFound


@bot.event
async def on_voice_state_update(member, before, after):
    """Function that auto changes user role on voice channel join and leave"""
    try:
        if str(after.channel) == 'Scrimming-VC':
            role = discord.utils.get(member.guild.roles, name="Player")
            await member.add_roles(role)
        elif str(before.channel) == 'Scrimming-VC':
            role = discord.utils.get(member.guild.roles, name="Player")
            await member.remove_roles(role)
    except AttributeError:
        pass


@bot.event
async def on_command_error(ctx, error):
    """Error message"""
    if isinstance(error, CommandNotFound):
        await ctx.send('Error: Command not found or spelled incorrectly')
        return
    raise error
