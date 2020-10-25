from bot.bot import bot
from utils.global_functions import findingstats
import os
import requests
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

tournyname = ''
tournystart = False


@bot.event
async def on_ready():
    """Print message when bot is ready"""
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    """Pre written messages that the bot will use to respond with"""
    if message.author == bot.user:
        return

    if 'marla' in message.content.lower() and 'love' in message.content.lower() \
            and str(message.author).split('#')[0].lower() != 'marley-ee':
        await message.channel.send("I'm with marley :/")

    if 'marla' in message.content.lower() and 'love' in message.content.lower() \
            and str(message.author).split('#')[0].lower() == 'marley-ee':
        await message.channel.send("I love you too!")

    if 'marla who created you?' in message.content.lower() or 'marla who created you' in message.content.lower() \
            or 'who created marla' in message.content.lower() or 'who made marla' in message.content.lower() \
            or 'who made marla bot' in message.content.lower() or 'who created marla bot' in message.content.lower() \
            or 'marla who made you?' in message.content.lower() or 'marla who made you' in message.content.lower():
        await message.channel.send('I was created by marley-EE!')

    if 'where is marley' in message.content.lower() or 'where is marley-ee' in message.content.lower() \
            or 'wheres marley' in message.content.lower() or "where's marley" in message.content.lower() \
            or 'wheres marley-ee' in message.content.lower() or "where's marley-ee" in message.content.lower():
        await message.channel.send('marley-EE is at the grocery store...')

    if 'how' in message.content.lower() and 'scrim' in message.content.lower():
        await message.channel.send('Scrims are just when we play against each other to get better. '
                                   'To join, you just hop into Scrimming-VC at the time the scrim is announced to be. '
                                   'From there, a scrim host will help coordinate everyone into the lobby. Check out '
                                   'this video for more details:\n '
                                   'https://www.youtube.com/watch?v=rXe-pqqpS0A&ab_channel=KrashyonSpellbreak')

    if 'how' in message.content.lower() and 'sign' in message.content.lower():
        await message.channel.send('Check the #tourney-info and #tourney-schedule channels for info how to sign-up')

    if message.attachments:
        if tournystart:
            if str(message.channel) == str(message.author).split('#')[0].lower():
                print('hi')
                await message.attachments[0].save(str(message.author).split('#')[0] + '.png')
                image = cv2.imread(str(message.author).split('#')[0] + '.png', 0)
                thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
                stats = findingstats(pytesseract.image_to_string(thresh, lang='eng', config='--psm 12', nice=1).split())

                try:
                    await message.channel.send(f'Player: {message.author} \nPlace: {stats[0]} \nExiles: {stats[1]}'
                                               f'\nAssists: {stats[2]} \nDamage: {stats[3]}')
                    file = open('element-info.txt', 'r')
                    out = file.readlines()
                    url = f"http://{out[2].strip()}:{out[3].strip()}/records"

                    payload = "{\r\n    \"data\": {\r\n        \"type\": \"record\",\r\n        \"attributes\": {\r\n     " \
                              f"       \"kills\": {stats[1]},\r\n            \"damage\": {stats[3]},\r\n            \"place\": 5," \
                              f"\r\n            \"assists\": {stats[2]},\r\n            \"username\": \"{message.author}\",\r\n            " \
                              f"\"game\": \"Game 1\",\r\n            \"discord_id\": {message.id},\r\n            " \
                              "\"scrimy_name\": \"\",\r\n            \"tourny_name\": \"Element 1\",\r\n            " \
                              f"\"qualy_name\": \"\",\r\n            \"score\": {3000}\r\n        " \
                              "}\r\n    }\r\n} "

                    headers = {
                        'Authorization': f'Basic {out[4].strip()}',
                        'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text.encode('utf8'))
                except:
                    print('except')
                    pass
                os.remove(str(message.author).split('#')[0] + '.png')
                # if str(message.attachments).split()[3].split("'")[1].endswith('.png'):
            else:
                pass
        else:
            pass
    await bot.process_commands(message)
