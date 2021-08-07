from google.cloud import vision
from dotenv import load_dotenv

import json
import random
import urllib

load_dotenv()

from module import Module


class google_tools(Module):
    async def send_image(self):
        args = self.ctx.content[1:].split(" ")
        API_KEY =  os.getenv('API_KEY')  # put your API key here
        SEARCH_ENGINE_ID = os.getenv('SEARCH_KEY')  # you also have to generate a search engine token
        start = 0
        q = ""
        if len(args) >= 1:
            for arg in args:
                q += urllib.parse.quote(str(arg)) + '+'
        found = False
        start = random.randint(1, 10)
        request = urllib.request.Request(
            'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +
            SEARCH_ENGINE_ID + '&q=' + q + '&start=' + str(start) + '&searchType=image&num=1')

        with urllib.request.urlopen(request) as f:
            if f != "":
                data = f.read().decode('utf-8')
                data = json.loads(data)
                if 'items' in data.keys():
                    url = data['items'][0]['link']
                    client = vision.ImageAnnotatorClient()
                    image = vision.Image()
                    image.source.image_uri = url

                    response = client.safe_search_detection(image=image)
                    safe = response.safe_search_annotation

                    flags = []
                    if safe.adult == 5:
                        flags.append("Adult")
                    if safe.violence == 5:
                        flags.append("Violence")
                    if len(flags) != 0:
                        await self.reply(":octagonal_sign: Flagged for " + ','.join(flags))
                        await self.reply("|| " + url +  " ||")
                    else: 
                        await self.reply(url)
                    
                    if response.error.message:
                        raise Exception(
                            '{}\nFor more info on error messages, check: '
                            'https://cloud.google.com/apis/design/errors'.format(
                                response.error.message))
                    found = True
            if not found:
                await self.reply("Could not find")
                # results = data['items']
