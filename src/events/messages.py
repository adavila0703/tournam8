from src.bot.bot import BOT as bot
from discord import Message
from src.ocr.ocr import ocr
import os
from src.state.tournament_state import TOURNAMENT_STATE as tournament_state

# TODO: Instead of saving the image, could just keep it in memory and use the OCR
# TODO: Clean this up, maybe override on_message() method
@bot.event
async def on_message(message: Message):
    """Event which handles reading the screenshot information"""
    if message.author == bot.user:
        return None

    await bot.process_commands(message)

    if message.attachments == []:
        return None

    channel = message.channel

    user = str(message.author).split('#')[0]
    category = str(message.channel.category).split('_')
    tournament_id = category[len(category) - 1]

    if not tournament_state.valid_tournament_player(tournament_id, user):
        return None
    
    path = './' + user + '.png'

    with open(path, 'w') as file:
    # TODO: Not checking if the incoming attachment is a png
        await message.attachments[0].save(path)
        stats = ocr(path)
        file.close()
        os.remove(path)
    
    tournament_state.record_player_stats(tournament_id, user, stats)
    await channel.send(f'User: {user} Game Stats: {stats}')
    return None
