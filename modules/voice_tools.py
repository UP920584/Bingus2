import datetime

from tinydb import TinyDB, Query
from discord.ext import tasks

from module import Module

db = TinyDB("db.json")

class voice_tools(Module):

    @tasks.loop(seconds = 1)
    async def check_requests(self):
        for request in db.all():
            if datetime.datetime.strptime(request['time'], "%Y%m%d%H%M%S")  < datetime.datetime.now():
                members = self.bot.get_all_members()
                for member in members:
                    if member.id == request['id']:
                        await member.move_to(None)
                Request = Query()
                db.remove(Request.id == request['id'])


    async def kick(self):
        for member in self.ctx.author.voice.channel.members:
            if member.mentioned_in(self.ctx):
                db.insert({
                    'time': (datetime.datetime.now() + datetime.timedelta(seconds=60)).strftime("%Y%m%d%H%M%S") ,
                    'id': member.id
                })


    async def unkick(self):
        Request = Query()
        query = Request.id == self.ctx.author.id
        if len(db.search(query)) != 0:
            db.remove(query)
            await self.reply("Aight bro, i won't")
        else: 
            await self.reply("I wasnt going to man wth")
