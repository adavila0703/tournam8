from discord.ext.commands import Bot
from dotenv import dotenv_values
from src.commands.tournament_commands import TournamentCommander

ENV = dotenv_values('.env')

BOT = Bot(command_prefix='!')
BOT.add_cog(TournamentCommander(BOT))
BOT.remove_command('help')

def run_bot():
    """Configs and runs discord bot"""
    BOT.run(ENV['DISCORD_TOKEN'])

