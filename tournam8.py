from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
import discord.utils
import os
import cv2
import pytesseract
from PIL import Image
import requests
import json
from requests.auth import HTTPBasicAuth
import time

bot = Bot(command_prefix='!')

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
stopocr = True

bot.remove_command('help')


def get_token():
    with open('token.txt', 'r') as g:
        lines = g.readlines()
        return lines[0].strip()


# none bot functions
def findingstats(num):
    storednums = 'First,Second,Third,Fourth,Fifth,Sixth,Seventh,Eighth,Ninth,Tenth,' \
                 'Eleventh,Twelfth,Thirteenth,Fourteenth,Fifteenth,Sixteenth,Seventeenth,' \
                 'Eighteenth,Nineteenth,Twentieth,Twenty-first,Twenty-second,Twenty-third,Twenty-fourth,' \
                 'Twenty-fifth,Twenty-sixth,Twenty-seventh,Twenty-eighth,Twenty-ninth,Thirtieth,Thirty-first,' \
                 'Thirty-second,Thirty-third,Thirty-fourth,Thirty-fifth,Thirty-sixth,Thirty-seventh,Thirty-eighth,' \
                 'Thirty-ninth,Fortieth,Forty-first,Forty-second,Forty-third,Forty-fourth,Forty-fifth,Forty-sixth,' \
                 'Forty-seventh,Forty-eighth,Forty-ninth,Fiftieth'
    splitnums = storednums.strip().upper().split(',')
    counting = 0
    for n in num:
        for s in splitnums:
            if n == s:
                return num[counting:counting + 4]
        counting += 1
    return 0


def checkchannels(channels, check):
    for c in channels:
        if str(c) == check:
            return True
    return False


# Bot functions
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if 'marla' in message.content.lower():
        await message.channel.send('Yes?')

    if 'best rune' in message.content.lower():
        await message.channel.send('Blink...')

    if 'blink' in message.content.lower():
        await message.channel.send('RIP Blink :(')

    if 'marla who created you?' in message.content.lower() or 'marla who created you' in message.content.lower() \
            or 'who created marla' in message.content.lower() or 'who made marla' in message.content.lower() \
            or 'who made marla bot' in message.content.lower() or 'who created marla bot' in message.content.lower() \
            or 'marla who made you?' in message.content.lower() or 'marla who made you' in message.content.lower():
        await message.channel.send('I was created by marley-EE!')

    if 'tell me a joke' in message.content.lower():
        print('nothing')

    # OCR
    if message.attachments:
        if stopocr != True:
            await message.attachments[0].save(str(message.author).split('#')[0] + '.png')
            image = cv2.imread(str(message.author).split('#')[0] + '.png', 0)
            thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
            stats = findingstats(pytesseract.image_to_string(thresh, lang='eng', config='--psm 12', nice=1).split())
            try:
                await message.channel.send(f'Player: {message.author} \nPlace: {stats[0]} \nExiles: {stats[1]}'
                                           f'\nAssists: {stats[2]} \nDamage: {stats[3]}')
            except:
                pass
            os.remove(str(message.author).split('#')[0] + '.png')
            # if str(message.attachments).split()[3].split("'")[1].endswith('.png'):
        else:
            pass
    await bot.process_commands(message)


# Change role on voice channel change
@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if str(after.channel) == 'Scrimming-VC':
            role = discord.utils.get(member.guild.roles, name="Player")
            await member.add_roles(role)
        elif str(after.channel) != 'Scrimming-VC':
            role = discord.utils.get(member.guild.roles, name="Player")
            await member.remove_roles(role)
    except AttributeError:
        pass


## BOT COMMANDS
@bot.command()
@has_permissions(administrator=True)
async def test(ctx, message):
    start_time = time.time()
    await ctx.send("--- %s seconds ---" % (time.time() - start_time))
    await ctx.send(message)


@bot.command()
@has_permissions(administrator=True)
async def makescreenshotchannel(ctx, vc_channel, category):
    start_time = time.time()
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
            nameout = c.mention
            text_out = discord.utils.get(ctx.guild.text_channels, name=name)
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
    await ctx.send(f'!makescreenshotchannel completed - exe time -> {time.time() - start_time}')


@bot.command()
@has_permissions(administrator=True)
async def deletechannels(ctx, category):
    start_time = time.time()
    category = discord.utils.get(ctx.guild.categories, name=category)
    for c in category.text_channels:
        await c.delete()
    await ctx.send(f'!deletechannels completed - exe time -> {time.time() - start_time}')


@bot.command()
@has_permissions(administrator=True, manage_roles=True)
async def giverole(member, role_name, vc_channel):
    start_time = time.time()
    fetch = discord.utils.get(member.guild.voice_channels, name=vc_channel)
    user = fetch.members
    role = discord.utils.get(member.guild.roles, name=role_name)
    for u in user:
        await u.add_roles(role)
    await member.send(f'!giverole completed - exe time -> {time.time() - start_time}')


@bot.command()
@has_permissions(administrator=True, manage_roles=True)
async def updatescrimroles(member, vc_channel):
    fetch = discord.utils.get(member.guild.voice_channels, name=vc_channel)
    user = fetch.members
    s1 = discord.utils.get(member.guild.roles, name='Scrimmed 1x')
    s2 = discord.utils.get(member.guild.roles, name='Scrimmed 2x')
    s3 = discord.utils.get(member.guild.roles, name='Scrimmed 3x')
    for u in user:
        for r in u.roles:
            if r == s1:
                await u.add_roles(s2)
                await u.remove_roles(s1)
            elif r == s2:
                await u.add_roles(s3)
                await u.remove_roles(s2)
                await u.remove_roles(s1)
            elif r == s3:
                await u.remove_roles(s1)
            else:
                await u.add_roles(s1)


@bot.command()
@has_permissions(administrator=True)
async def removeallscrimroles(member):
    fetch = member.guild.members
    s1 = discord.utils.get(member.guild.roles, name='Scrimmed 1x')
    s2 = discord.utils.get(member.guild.roles, name='Scrimmed 2x')
    s3 = discord.utils.get(member.guild.roles, name='Scrimmed 3x')
    for f in fetch:
        for r in f.roles:
            if r == s1 or r == s2 or r == s3:
                await f.remove_roles(s1)
                await f.remove_roles(s2)
                await f.remove_roles(s3)


@bot.command()
@has_permissions(administrator=True, manage_roles=True)
async def help(member):
    await member.send("```Help Menu\nHow to use: !func(p1, p2) will be written out like !func p1 p2, for spaces use"
                      "quotes!\n\n"
                      "-!makescreenshotchannel(vc_channel, category) - Creates a text channel for all the users "
                      "inside a specified voice channel\n\n"
                      "-!deletechannels(category) - Deletes all text channels in a selected category.\n\n"
                      "-!giverole(role_name, vc_channel) - Give everyone in a specified voice chat a role of "
                      "choice.\n\n "
                      "-!updatescrimroles(vc_channel) - Gives a user the 'scrimmed role'(x1, x2, x3) Example: If they "
                      "have x1 and you run the function, then x1 will be deleted and x2 will be added.\n\n"
                      "-!removeallscrimroles - Removes all scrim roles from everyone who owns the role.\n\n"
                      "** Marla bot was created by marley-EE **```")


# BOT Command errors
@makescreenshotchannel.error
async def makescreenshotchannel_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Error: You are missing your arguments')
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Error: No members in the channel or channel doesnt exist.')


@deletechannels.error
async def deletechannels_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Error: You are missing your arguments')
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Error: No channels or category doesnt exist.')


# @giverole.error
# async def giverole_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Error: You are missing your arguments')
#     if isinstance(error, commands.CommandInvokeError):
#         await ctx.send('Error: No channels or category doesnt exist.')

@updatescrimroles.error
async def updatescrimroles_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Error: You are missing your arguments')
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Error: Role might not exist.')


url = "http://localhost:5000/users"

# payload = "{\n    \"data\":\n    {\n    \"type\":\"user\", \"attributes\":\n        {\n
# \"username\":\"Angel\", \n        \"discordname\":\"\"\n\n        }\n    }\n}"
payload = "{\n    \"data\":\n    {\n    \"type\":\"user\", \"attributes\":\n        {\n        " \
          "\"username\":\"Angel\", \n        \"discordname\":\"\"\n\n        }\n    }\n} "
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic dGl0bzp0aXRv',
    'Authorization': 'Basic dGl0bzp0aXRv',
    'Content-Type': 'text/plain'
}

# get json data
# response = requests.request("GET", url, headers=headers, data=payload)
# read = json.loads(response.text)
# data = read['data']
#
# for d in data:
#     print(d['attributes']['username'].lower())

bot.run(get_token())
