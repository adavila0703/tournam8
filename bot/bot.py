from discord.ext.commands import Bot

bot = Bot(command_prefix='!')
bot.remove_command('help')