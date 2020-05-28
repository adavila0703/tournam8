import cv2
import pytesseract
from discord.ext.commands import Bot
from PIL import Image
import os

bot = Bot(command_prefix='!')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


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


# bot functions
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('boo')

    if message.content.startswith('wtf'):
        await message.guild.create_text_channel('hi')
        await message.channel.send('Wow, stay calm')

    if message.content.startswith('is anyone on'):
        await message.channel.send('Me, but im a bot.')

    if message.content.startswith('fuck you'):
        await message.channel.send('Fuck me? Fuck you.')

    if message.content.startswith('who is marley'):
        await message.channel.send('Global Elite')

    if message.content.startswith('thank you marleybot'):
        await message.channel.send('Got you bro')

    if message.content.startswith('marleybot is corey op'):
        await message.channel.send('No')

    if message.content.startswith('marleybot'):
        await message.channel.send('BRB')

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


# bot commands
@bot.command(options='hello')
async def startgame(ctx, game):
    if checkchannels(ctx.guild.text_channels, game) == True:
        await ctx.send('Channel Already Exists')
    else:
        await ctx.guild.create_text_channel(game)
        await ctx.send('Starting Game')


@bot.command()
async def sendchannel(ctx, game):
    print()


bot.run(get_token())
