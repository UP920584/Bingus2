import os
import datetime
import string
import re
from asyncio import get_event_loop
from aiohttp.web import AppRunner, Application, TCPSite
# API
import base64
import aiohttp_jinja2
import jinja2

from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from dotenv import load_dotenv
# Bot Resources
import discord
from discord.ext import tasks

from module import Module
from modules.google_tools import google_tools
from modules.spoilers import spoilers
from modules.inspiro import inspiro
from modules.voice_tools import voice_tools
from modules.time_tools import time_tools

gt = google_tools()
vt = voice_tools()
spoilers = spoilers()
inspiro = inspiro()
time = time_tools()

from api import routes

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True
bot = discord.Client(intents=intents)

Module.bot = bot
vt.check_requests.start()
time.check_reminders.start()

@bot.event
async def on_ready():
    await bot.change_presence(activity= discord.Activity(type=discord.ActivityType.playing,name="\"bingus help\" for commands"))


@bot.event
async def on_message(message):
    try: 
        content = message.content.strip("'")
        
        Module.ctx = message
        reply = Module.reply = message.channel.send 
        if content != "":
            if message.author != bot.user:
                if content[0] == "-":
                    print("test")
                    await gt.send_image()
                elif content == "spoiler this":
                    await spoilers.spoiler()
                elif content == "send inspiro":
                    await inspiro.get_inspiro()
                elif content.startswith("kick"):
                    await vt.kick()
                elif content == "dont kick me":
                    await vt.unkick()
                elif content == "bingus help":
                    await reply("""
<a:CatPop:795041308615901256> search for images with a dash eg: "__-bingus__" would search for images of bingus
<:catpray:872895629691617320> send an inspiring image from inspiro bot with "__send inspiro__"
<:pcSir:795041433915752519> spoiler an image or text by replying with "__spoiler this__"
<:WiseChamp:795041234938363905> attempt to kick someone with "kick @person" if you dont wanna be kicked just say "dont kick me" 
<:ping:896003097653051425> set a reminder for a message by replying to it like "remind in in 1 minute bingus" or "remind me in 12 hours bingus" 
                    """)
                elif re.match("^remind me in [1-9][0-9]{0,3} (minute)?(hour)?s? bingus", content):
                    params = content.split(' ')
                    await time.create_reminder(int(params[3]) * (60 if params[4].strip('s') == "minute" else 3600))
                    await reply("reminder set <:blusho:896004717820391424>")
                elif content == "testing123":
                    await time.check_reminders()
                    #await bot. message.author.edit(voice_channel=None)
    except Exception as e:
        dev = message.guild.get_member(312612747898650625)
        await dev.send(e)




async def run_bot():

    app = Application()
    app.add_routes(routes)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),"templates")))
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, '0.0.0.0', 3000)
    await site.start()

    app['bot'] = bot
    
    try:
        await bot.start(TOKEN)
        #bot.loop.create_task(check_requests())
    except:
        await bot.close(),
        raise

    finally:
        await runner.cleanup()

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(run_bot())


