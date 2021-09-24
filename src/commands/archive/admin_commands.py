from src.bot.bot import BOT as bot
from discord.ext.commands import has_permissions, Context
import time
import discord.utils
import src.utils.logger as logger
from src.state.player_list_state import PLAYER_LIST
from src.utils.output_message import OUTPUTS

@bot.command()
@has_permissions(administrator=True)
async def make_screenshot_channel(
    ctx: Context, 
    vc_channel: str, 
    category: str, 
    player_list = PLAYER_LIST,
    discord_utils = discord.utils
) -> Context.send:
    """Command that creates a text channel for all current users in a specified voice chat"""

    await ctx.send('Executing !make_screenshots_channel')

    start_time = time.time()
    channel = discord_utils.get(ctx.guild.voice_channels, name=vc_channel)
    target_category = discord_utils.get(ctx.guild.categories, name=category)
    text_channels = set(map(lambda text_channel: text_channel.name, ctx.guild.text_channels))

    if target_category is None:
        await ctx.send('Category doesnt exist')
        return None
    
    for member in channel.members:
        member_name = str(member).split('#')[0].lower()

        if member_name in text_channels:
            continue

        player_list.add_player_to_list(member_name)

        await ctx.guild.create_text_channel(member_name, category=target_category)

        try:
            await logger.message_to_channel(ctx, f' Welcome {member.mention}!' + OUTPUTS['SCREENSHOT'], member_name)
            await logger.file_to_channel(ctx, member_name, discord.File('./tempss.png'))
            await logger.message_to_channel(ctx, OUTPUTS['TIPS'], member_name)
        except AttributeError:
            await logger.message_to_channel(ctx, 'Cant accept special characters a players name.', None)
        except FileNotFoundError:
            await logger.message_to_channel(ctx, 'Template screenshot file not found, please contact admin', None)
    await logger.message_to_channel(ctx, f'!make_screenshots_channel Completed! - Execution Time: {time.time() - start_time}s', None)

@bot.command()
@has_permissions(administrator=True)
async def delete_ss_channels(
    ctx: Context, 
    player_list = PLAYER_LIST,
    discord_utils = discord.utils
) -> Context.send:
    """Deletes channels within a given category"""
    start_time = time.time()
    await ctx.send('Executing !delete_ss_channels')

    for player in player_list.players:
        channel_name = player.strip()
        channel = discord_utils.get(ctx.guild.text_channels, name=channel_name)

        if channel == None:
            continue

        await channel.delete()
        
    player_list.clear_player_list()
    
    await ctx.send(f'!delete_ss_channels Completed! - Execution Time: {time.time() - start_time}s')
