from discord.ext.commands import Context

class UserCommander():
    def __init__(
        self, 
        bot
    ) -> None:
        self.bot = bot

    # @commands.command()
    async def get_stats(
        self,
        ctx: Context
    ) -> Context.send:
        """Creates a tournament"""
        pass