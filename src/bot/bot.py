from discord.ext.commands import Bot
from src.vars.vars import Env
from src.commands.tournament_commands import TournamentCommander
from src.events.messages import MessageCoordinator


BOT = Bot(command_prefix='!')
# TODO: Need to add message and user_commmand cog to bot 
BOT.add_cog(TournamentCommander(BOT))
BOT.add_cog(MessageCoordinator(BOT))
BOT.remove_command('help')

def run_bot():
    """Configs and runs discord bot"""
    BOT.run(Env.DISCORD_TOKEN.value)

