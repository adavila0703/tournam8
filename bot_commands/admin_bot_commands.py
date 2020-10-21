from bot.bot import bot
from discord.ext.commands import has_permissions
import requests
import json
from requests.auth import HTTPBasicAuth
import time
import discord.utils


@bot.command()
@has_permissions(administrator=True)
async def testingpost(ctx):
    """Test function to send information to the database"""
    ply = ctx.author.id
    print(ply)
    url = "http://localhost:5000/records"

    payload = "{\r\n    \"data\":\r\n    {\r\n    \"type\":\"user\", \"attributes\":\r\n        {\r\n        " \
              "\"username\":\"test\", \r\n        \"discordname\":\"test\"\r\n\r\n        }\r\n    }\r\n} "
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic dGl0bzp0aXRv'
    }

    filter = '''{"name":"discord_id", "op":"eq", "val":"''' + "{a}".format(a=ply) + '''"}'''

    r = requests.get(url + f"?filter=[{filter}]", auth=HTTPBasicAuth('tito', 'tito'))
    read = json.loads(r.text)
    data = read['data']
    kills = 0
    assists = 0
    damage = 0

    for d in data:
        kills += int(d['attributes']['kills'])

    for d in data:
        assists += int(d['attributes']['assists'])

    for d in data:
        damage += int(d['attributes']['damage'])

    await ctx.send('Kills: {a}\nAssists: {b}\nTotal Damage:{c}'.format(a=kills, b=assists, c=damage))


@bot.command()
@has_permissions(administrator=True)
async def getstats(ctx, player):
    """Command to get stats from database using an api"""
    ply = player.split('!')[1].replace('>', '')
    file = open('element-info.txt', 'r')
    out = file.readlines()
    url = f"http://{out[2].strip()}:{out[3].strip()}/records"

    filter = '''{"name":"discord_id", "op":"eq", "val":"''' + "{a}".format(a=ply) + '''"}'''

    r = requests.get(url + f"?filter=[{filter}]", auth=HTTPBasicAuth(f'{out[0].strip()}', f'{out[1].strip()}'))
    file.close()
    read = json.loads(r.text)
    data = read['data']
    kills = 0
    assists = 0
    damage = 0

    for d in data:
        kills += int(d['attributes']['kills'])

    for d in data:
        assists += int(d['attributes']['assists'])

    for d in data:
        damage += int(d['attributes']['damage'])

    await ctx.send('Kills: {a}\nAssists: {b}\nTotal Damage:{c}'.format(a=kills, b=assists, c=damage))


@bot.command()
@has_permissions(administrator=True)
async def testget(ctx):
    """Another testing get function"""
    url = "http://localhost:5000/users"

    payload = "{\r\n    \"data\":\r\n    {\r\n    \"type\":\"tourns\", \r\n    \"attributes\":\r\n        {\r\n       " \
              " \"name\": \"element 4\"\r\n\r\n        }\r\n    }\r\n} "
    headers = {
        'Authorization': 'Basic dGl0bzp0aXRv',
        'Content-Type': 'application/json'
    }

    # response = requests.request("GET", url, headers=headers, data=payload)

    filter = '''{"name":"username", "op":"eq", "val":"marley"}'''
    r = requests.get(url + f"?filter=[{filter}]", auth=HTTPBasicAuth('tito', 'tito'))

    read = json.loads(r.text)
    # data = read['data']
    #
    # score = 0
    # discord_name = 'marley'
    # for d in data:
    #     d['attributes']['score'] += score
    # return None
    #
    # print(discord_name + '-' + score)
    #
    # print(read)


@bot.command()
@has_permissions(administrator=True)
async def testpost(ctx):
    """Testing post to database"""
    url = "http://localhost:5000/users"

    payload = "{\r\n    \"data\":\r\n    {\r\n    \"type\":\"user\", \"attributes\":\r\n        {\r\n        " \
              "\"username\":\"rip\", \r\n        \"discordname\":\"hello\"\r\n\r\n        }\r\n    }\r\n} "
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic dGl0bzp0aXRv'
    }

    requests.request("POST", url, headers=headers, data=payload)
    return None


@bot.command()
@has_permissions(administrator=True)
async def starttournament(ctx, name):
    """Experimental start tournament command"""
    global tournyname, tournystart
    file = open('players.txt', 'r')
    if tournystart == False:
        tournystart = True
        tournyname = name
        print(tournyname)
        await ctx.send(f'Starting tournment {tournyname}')
        for f in file.readlines():
            text_out = discord.utils.get(ctx.guild.text_channels, name=f.split('\n')[0])
            await text_out.send('Tournment is starting! Only the screenshot that relates to the game you are'
                                'currently playing.\n\n'
                                '---------- Game 1 ----------')

    else:
        await ctx.send('There is already a tournment in progress')


@bot.command()
@has_permissions(administrator=True)
async def makescreenshotchannel(ctx, vc_channel, category):
    """Command that makes a text channel for all users in a given voice chat"""
    await ctx.send('Executing !makescreenshotchannel')
    start_time = time.time()
    file = open('players.txt', 'w')
    channel = discord.utils.get(ctx.guild.voice_channels, name=vc_channel)
    get_text_channels = ctx.guild.text_channels
    if discord.utils.get(ctx.guild.categories, name=category) is None:
        await ctx.send('Category doesnt exist')
    else:
        for c in channel.members:
            for g in get_text_channels:
                if str(c).split('#')[0].lower() == str(g):
                    return None
                else:
                    pass
            await ctx.guild.create_text_channel(str(c).split('#')[0],
                                                category=discord.utils.get(ctx.guild.categories, name=category))
            name = str(c).split('#')[0].lower()
            file.writelines(name + '\n')
            nameout = c.mention
            text_out = discord.utils.get(ctx.guild.text_channels, name=name)
            try:
                await text_out.send(
                    f'Welcome {nameout}! This is the channel where you will be posting your screenshots,'
                    f'dont forget!\n\nOne of my major features is the ability to read the'
                    f' information from your screenshot, make sure you get a good picture of your stats'
                    f' after your game, the better the picture, the more accurate I will be!'
                    f'\n\nBelow is an and example of the screen you need to capture after your '
                    f'Spellbreak '
                    f'match!\n\nGood luck today Breaker!\n\n -Marla')
                await text_out.send(file=discord.File('marley.png'))
                await text_out.send('Tip: ALT + PRINTSCREEN will take a picture of the monitor your mouse is currently'
                                    'active on. \n\nCTL + v into the discord message will send the picture you just '
                                    'took.')
            except AttributeError:
                await ctx.send('Cant accept special characters a players name.')
                pass
    await ctx.send(f'!makescreenshotchannel Completed! - Execution Time: {time.time() - start_time}s')


@bot.command()
@has_permissions(administrator=True)
async def old_deletechannels(ctx, category):
    """OLD command to delete channels in a given category"""
    file = open('players.txt', 'r')
    await ctx.send('Executing !deletechannels')
    start_time = time.time()
    category = discord.utils.get(ctx.guild.categories, name=category)
    for c in category.text_channels:
        await c.delete()
    await ctx.send(f'!deletechannels Completed! - Execution Time: {time.time() - start_time}s')


@bot.command()
@has_permissions(administrator=True)
async def deletechannels(ctx):
    """NEW command to delete channels in a given category"""
    file = open('players.txt', 'r')
    await ctx.send('Executing !deletechannels')
    start_time = time.time()
    for a in file.readlines():
        channame = a.strip().replace('\n', '')
        channel = discord.utils.get(ctx.guild.text_channels, name=channame)
        await channel.delete()
    await ctx.send(f'!deletechannels Completed! - Execution Time: {time.time() - start_time}s')
