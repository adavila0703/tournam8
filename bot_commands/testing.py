from bot.bot import bot
import discord.utils
import time
from discord.ext.commands.errors import CommandInvokeError



@bot.command()
async def roles(ctx):
    """Command to update players scrim role"""
    await ctx.send('Executing !updatescrimroles')
    start_time = time.time()
    s1 = discord.utils.get(ctx.guild.roles, name='Scrimmed 1x')
    s2 = discord.utils.get(ctx.guild.roles, name='Scrimmed 2x')
    s3 = discord.utils.get(ctx.guild.roles, name='Scrimmed 3x')

    for member in s3.members:
        await member.remove_roles(s3)
    for member in s2.members:
        await member.remove_roles(s2)
    for member in s1.members:
        await member.remove_roles(s1)

    await ctx.send(f'!updatescrimroles Completed! - Execution Time: {time.time() - start_time}s')
