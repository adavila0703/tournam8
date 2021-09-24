from discord.ext.commands import Context
from discord.ext import commands

class UserCommander(commands.Cog):
    def __init__(
        self, 
        bot
    ) -> None:
        self.bot = bot

    @commands.command()
    async def get_stats(
        self,
        ctx: Context
    ) -> Context.send:
        """Creates a tournament"""
        pass