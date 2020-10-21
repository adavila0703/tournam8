from bot.bot import bot
import discord.utils

# function that changes user role on voice channel join and leave
@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if str(after.channel) == 'Scrimming-VC':
            role = discord.utils.get(member.guild.roles, name="Player")
            await member.add_roles(role)
        elif str(before.channel) == 'Scrimming-VC':
            role = discord.utils.get(member.guild.roles, name="Player")
            await member.remove_roles(role)
    except AttributeError:
        pass