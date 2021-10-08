import datetime

from tinydb import TinyDB, Query
from discord.ext import tasks

import discord
from module import Module

db = TinyDB("reminders.json")

class time_tools(Module):


    @tasks.loop(seconds = 1)
    async def check_reminders(self):
        for reminder in db.all():
            if datetime.datetime.strptime(reminder['time'], "%Y%m%d%H%M%S") < datetime.datetime.now():
                channels = self.bot.get_all_channels()
                for channel in channels: 
                    if channel.id == reminder['channel']:
                        old = await channel.fetch_message(reminder['ref'])
                        await old.reply('Reminder', mention_author=True)
                        ReminderDto = Query()
                        db.remove(ReminderDto.ref == reminder['ref'])


    async def create_reminder(self, time):
        record = {
            'time': (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y%m%d%H%M%S") ,
            'ref': self.ctx.reference.message_id,
            'id': self.ctx.author.id,
            'channel': self.ctx.channel.id
        }
        db.insert(record)


    async def delete_reminders(self):
        ReminderDto = Query()
        query = ReminderDto.id == self.ctx.author.id
        if len(db.search(query)) != 0:
            reminders.remove(query)
            await self.reply("Aight bro, i won't")
        else: 
            await self.reply("You dont got any reminders")