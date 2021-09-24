from bot.bot import bot
import discord.utils
import time


@bot.command()
async def test(ctx, channel, category):
    """Command to update players scrim role"""
    await ctx.send('Executing !test')
    start_time = time.time()

    await ctx.guild.create_text_channel(channel, category=discord.utils.get(ctx.guild.categories, name=category))

    text_out = discord.utils.get(ctx.guild.text_channels, name=channel)
    await text_out.send('Hello')

    await ctx.send(f'!test Completed! - Execution Time: {time.time() - start_time}s')
