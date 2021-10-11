import discord
import asyncio

from module import Module

class music(Module):

    async def play(self, song):
        state = self.ctx.author.voice
        if state:
            vc = await state.channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="lib/ffmpeg.exe", source="resources/" + song))
            while vc.is_playing():  
                await asyncio.sleep(1)  
            else:
                await asyncio.sleep(15)  
                while vc.is_playing():  
                    break  
                else:
                    await vc.disconnect()  
        else: 
            await self.reply("please run this command while in a voice channel in " + self.ctx.guild.name)

    async def close(self):
        for x in self.bot.voice_clients:
            if(x.guild == self.ctx.guild):
                return await x.disconnect()