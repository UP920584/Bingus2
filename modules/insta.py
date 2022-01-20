from module import Module
from tinydb import TinyDB, Query

import json
import time
import random
import urllib.request
from urllib.request import Request, urlopen

db = TinyDB("sources.json")

class insta(Module):
    
    def get_post(self, name): 
        PostDto = Query()
        query = db.search(PostDto.name == name)
        if(len(query) == 0):
            return self.reply("cant find anything for this :((")
        
        decoded = urlopen(query[0]["url"]).read().decode('utf8').strip("'")
        array = json.loads(decoded)
        url = array[random.randint(0, len(array))]
        if "instagram" in url:
            req = urlopen(url + "media") 
            url = req.geturl()

        return self.reply(url)

    def get_random(self):
        query = db.all()
        self.get_post(query[random.randint(0, len(query))].name)

    def upsert_pool(self, name, url):
        Pool = Query()
        pool = {
            'url': url,
            'name': name
        }
        db.upsert(pool, Pool.name == name)