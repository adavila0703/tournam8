# from src.bot.bot import BOT as bot
# from discord.ext.commands import has_permissions
# import time
# import discord.utils
# from src.utils.role_check import check_s1, check_s2, check_s3


# @bot.command()
# @has_permissions(manage_roles=True)
# async def give_role(ctx, role_name, vc_channel):
#     """Command to give role to players"""
#     await ctx.send('Executing !giverole')
#     start_time = time.time()
#     fetch = discord.utils.get(ctx.guild.voice_channels, name=vc_channel)
#     user = fetch.members
#     role = discord.utils.get(ctx.guild.roles, name=role_name)
#     for u in user:
#         await u.add_roles(role)
#     await ctx.send(f'!giverole Completed! - Execution Time: {time.time() - start_time}s')

# @bot.command()
# @has_permissions(manage_roles=True)
# async def update_scrimroles(ctx):
#     """Command to update players scrim role"""
#     await ctx.send('Executing !updatescrimroles')
#     start_time = time.time()
#     channels = ctx.guild.voice_channels
#     s1 = discord.utils.get(ctx.guild.roles, name='Scrimmed 1x')
#     s2 = discord.utils.get(ctx.guild.roles, name='Scrimmed 2x')
#     s3 = discord.utils.get(ctx.guild.roles, name='Scrimmed 3x')

#     for channel in channels:
#         for member in channel.members:
#             if s3 not in member.roles and s2 not in member.roles and s1 not in member.roles:
#                 await member.add_roles(s1)
#             elif s1 in member.roles:
#                 await member.add_roles(s2)
#                 await member.remove_roles(s1)
#             elif s2 in member.roles:
#                 await member.add_roles(s3)
#                 await member.remove_roles(s2)

#     await ctx.send(f'!updatescrimroles Completed! - Execution Time: {time.time() - start_time}s')



# @bot.command()
# @has_permissions(manage_roles=True)
# async def remove_all_scrimroles(ctx):
#     """Function to remove all scrim roles from players that had the scrim role"""
#     await ctx.send('Executing !removeallscrimroles')
#     start_time = time.time()
#     s1 = discord.utils.get(ctx.guild.roles, name='Scrimmed 1x')
#     s2 = discord.utils.get(ctx.guild.roles, name='Scrimmed 2x')
#     s3 = discord.utils.get(ctx.guild.roles, name='Scrimmed 3x')

#     for member in s3.members:
#         await member.remove_roles(s3)
#     for member in s2.members:
#         await member.remove_roles(s2)
#     for member in s1.members:
#         await member.remove_roles(s1)

#     await ctx.send(f'!removeallscrimroles Completed! - Execution Time: {time.time() - start_time}s')


# @bot.command()
# @has_permissions(manage_roles=True)
# async def help(member):
#     """Help command which shows all the available utils"""
#     await member.send("```                            Help Menu\n"
#                       "\nHow to use: !func(p1, p2) will be written out like !func p1 p2, for spaces use"
#                       "quotes!\n\n"
#                       "-!makescreenshotchannel(vc_channel, category) - Creates a text channel for all the users "
#                       "inside a specified voice channel\n\n"
#                       "-!deletechannels(category) - Deletes all text channels in a selected category.\n\n"
#                       "-!giverole(role_name, vc_channel) - Give everyone in a specified voice chat a role of "
#                       "choice.\n\n "
#                       "-!updatescrimroles - Gives a user the 'scrim role'(x1, x2, x3) Example: If they "
#                       "have x1 and you run the function, then x1 will be deleted and x2 will be added.\n\n"
#                       "-!removeallscrimroles - Removes all scrim roles from everyone who owns the role.\n\n"
#                       "** Marla bot was created by marley-EE **```")
