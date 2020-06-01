import cv2
import pytesseract
from discord.ext.commands import Bot, has_permissions, MissingPermissions
import discord.utils
from discord import Guild
from PIL import Image
import os
import requests
import json
from requests.auth import HTTPBasicAuth

bot = Bot(command_prefix='!')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

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

    if message.content.startswith('hi'):
        await message.channel.send('boo')


    if message.content.startswith('marleybot'):
        await message.channel.send('BRB')

    # OCR
    if message.attachments:
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
    await bot.process_commands(message)


# Change role on voice channel change
@bot.event
async def on_voice_state_update(member, before, after):
    if str(after.channel) == 'Scrimming Vc':
        role = discord.utils.get(member.guild.roles, name="badass")
        await member.add_roles(role)
    elif str(after.channel) != 'Scrimming Vc':
        role = discord.utils.get(member.guild.roles, name="badass")
        await member.remove_roles(role)


## BOT COMMANDS

@bot.command()
@has_permissions(administrator=True)
async def test(ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name='marley-ee')
    await channel.send(file=discord.File('marley.png'))

@bot.command()
@has_permissions(administrator=True)
async def makescreenshotchannel(ctx, vc_channel, category):
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
            pic = discord.File('marley.png')
            text_out = discord.utils.get(ctx.guild.text_channels, name=name)
            await text_out.send(f'Welcome {nameout}! This is the channel where you will be posting your screenshots, '
                                f'dont forget!\n\nOne of my major features is the ability to read the'
                                f' information from your screenshot, make sure you get a good picture of your stats'
                                f' after your game, the better the picture, the more accurate I will be!'
                                f'\n\nBelow is an and example of the screen you need to capture after your Spellbreak '
                                f'match!\n\nGood luck today Breaker!\n\n -Marla')
            await text_out.send(file=discord.File('marley.png'))
            await text_out.send('Tip: ALT + PRINTSCREEN will take a picture of the monitor your mouse is currently'
                                ' active on. \n\nCTL + v into the discord message will send the picture you just took.')

            file = open('channels.txt', 'r+')
            file.writelines(str(c).split('#')[0].lower() + ' \n')



@bot.command()
@has_permissions(administrator=True)
async def deletescreenshotchannels(ctx):
    channel = ctx.guild.text_channels
    for c in channel:
        file = open('channels.txt', 'r+')
        # for f in file.readlines():
        #     if f.split()[0] == str(c):
        #         await
        #     else:
        #         pass


@bot.command()
@has_permissions(administrator=True, manage_roles=True)
async def giverole(member, role_name, vc_channel):
    fetch = discord.utils.get(member.guild.voice_channels, name=vc_channel)
    user = fetch.members
    role = discord.utils.get(member.guild.roles, name=role_name)
    for u in user:
        await u.add_roles(role)


@bot.command()
@has_permissions(administrator=True, manage_roles=True)
async def updatescrimroles(member, vc_channel):
    fetch = discord.utils.get(member.guild.voice_channels, name=vc_channel)
    user = fetch.members
    s1 = discord.utils.get(member.guild.roles, name='scrimmed x1')
    s2 = discord.utils.get(member.guild.roles, name='scrimmed x2')
    s3 = discord.utils.get(member.guild.roles, name='scrimmed x3')
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
    s1 = discord.utils.get(member.guild.roles, name='scrimmed x1')
    s2 = discord.utils.get(member.guild.roles, name='scrimmed x2')
    s3 = discord.utils.get(member.guild.roles, name='scrimmed x3')
    for f in fetch:
        for r in f.roles:
            if r == s1 or r == s2 or r == s3:
                await f.remove_roles(s1)
                await f.remove_roles(s2)
                await f.remove_roles(s3)


@bot.command()
@has_permissions(administrator=True, manage_roles=True)
async def help(member):
    await member.send("```"
                   "-!makescreenshotchannel(vc_channel, category) - Creates a text channel for all the users "
                   "inside a specified voice channel\n\n"
                   "-!deletescreenshotchannels - Deletes all the screenshot channels that were previously made\n\n"
                   "-!giverole(role_name, vc_channel) - Give everyone in a specified voice chat a role of choice.\n\n"
                   "-!updatescrimroles(vc_channel) - Gives a user the 'scrimmed role'(x1, x2, x3) Example: If they have"
                   "x1 and you run the function, then x1 will be deleted and x2 will be added.\n\n"
                   "-!removeallscrimroles - Removes all scrim roles from everyone who owns the role, in your channel.\n\n```")


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
