import urllib.request
import discord

from module import Module

class spoilers(Module):

    async def spoiler(self):
        if self.ctx.reference is not None:
            old = await self.ctx.channel.fetch_message(self.ctx.reference.message_id)
            if old.content == "":
                if len(old.attachments) != 0:
                    image_types = ["png", "jpeg", "gif", "jpg"]
                    for attachment in old.attachments:
                        if any(attachment.filename.lower().endswith(image) for image in image_types):
                            spoiled = await attachment.to_file(spoiler=True)
                            await self.reply(file=spoiled)
                            await old.delete()
                else:
                    await self.reply("nothing to spoiler")
            else:
                content = old.content
                await old.delete()
                await self.reply( "|| " + content + " ||")
            
                