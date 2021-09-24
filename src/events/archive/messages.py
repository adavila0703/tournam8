# from src.bot.bot import BOT as bot




# @bot.event
# async def on_message(message):
#     """Pre written messages that the bot will use to respond with"""
#     if message.author == bot.user:
#         return

#     if 'marla' in message.content.lower() and 'love' in message.content.lower() \
#             and str(message.author).split('#')[0].lower() != 'marley-ee':
#         await message.channel.send("I'm with marley :/")

#     if 'marla' in message.content.lower() and 'love' in message.content.lower() \
#             and str(message.author).split('#')[0].lower() == 'marley-ee':
#         await message.channel.send("I love you too!")

#     if 'marla who created you?' in message.content.lower() or 'marla who created you' in message.content.lower() \
#             or 'who created marla' in message.content.lower() or 'who made marla' in message.content.lower() \
#             or 'who made marla bot' in message.content.lower() or 'who created marla bot' in message.content.lower() \
#             or 'marla who made you?' in message.content.lower() or 'marla who made you' in message.content.lower():
#         await message.channel.send('I was created by marley-EE!')

#     if 'where is marley' in message.content.lower() or 'where is marley-ee' in message.content.lower() \
#             or 'wheres marley' in message.content.lower() or "where's marley" in message.content.lower() \
#             or 'wheres marley-ee' in message.content.lower() or "where's marley-ee" in message.content.lower():
#         await message.channel.send('marley-EE is at the grocery store...')

#     if 'how' in message.content.lower() and 'scrim' in message.content.lower():
#         await message.channel.send('Scrims are just when we play against each other to get better. '
#                                    'To join, you just hop into Scrimming-VC at the time the scrim is announced to be. '
#                                    'From there, a scrim host will help coordinate everyone into the lobby. Check out '
#                                    'this video for more details:\n '
#                                    'https://www.youtube.com/watch?v=rXe-pqqpS0A&ab_channel=KrashyonSpellbreak')

#     if 'how' in message.content.lower() and 'sign' in message.content.lower():
#         await message.channel.send('Check the #tourney-info and #tourney-schedule channels for info how to sign-up')

#     await bot.process_commands(message)
