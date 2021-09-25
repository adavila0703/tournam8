from discord.ext.commands import Bot
from src.dotenv.dotenv import ENV
from src.commands.tournament_commands import TournamentCommander


BOT = Bot(command_prefix='!')
# TODO: Need to add message and user_commmand cog to bot 
BOT.add_cog(TournamentCommander(BOT))
BOT.remove_command('help')

def run_bot():
    """Configs and runs discord bot"""
    BOT.run(ENV['DISCORD_TOKEN'])

