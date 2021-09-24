from bot_commands.admin_bot_commands import makescreenshotchannel, deletechannels
from bot_commands.staff_bot_commands import updatescrimroles
from discord.ext.commands import MissingRequiredArgument, CommandInvokeError


@makescreenshotchannel.error
async def makescreenshotchannel_error(ctx, error):
    """Error message for makescreenshotchannel command"""
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Error: You are missing your arguments')
    if isinstance(error, CommandInvokeError):
        await ctx.send('Error Possibilities: -No users in the channel\n-Category or channel doesnt exist\n '
                       '-Bot doesnt have permissions')


@deletechannels.error
async def deletechannels_error(ctx, error):
    """Error message for deletechannels command"""
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Error: You are missing your arguments')
    if isinstance(error, CommandInvokeError):
        await ctx.send('Error: No channels or category doesnt exist.')


@updatescrimroles.error
async def updatescrimroles_error(ctx, error):
    """Error message for updatescrimroles command"""
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Error: You are missing your arguments')
    if isinstance(error, CommandInvokeError):
        await ctx.send('Error: Role might not exist.')


# @giverole.error
# async def giverole_error(ctx, error):
#     if isinstance(error, utils.MissingRequiredArgument):
#         await ctx.send('Error: You are missing your arguments')
#     if isinstance(error, utils.CommandInvokeError):
#         await ctx.send('Error: No channels or category doesnt exist.')

