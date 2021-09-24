from src.bot.bot import BOT as bot

@bot.event
async def on_ready():
    """Print message when bot is ready"""
    print(f'We have logged in as {bot.user}')