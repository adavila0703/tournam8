from discord.ext.commands import Bot
from utils.global_functions import get_token

bot = Bot(command_prefix='!')
bot.remove_command('help')


def runbot():
    """Run bot function (being called in app.py)"""
    bot.run(get_token())
