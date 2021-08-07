from aiohttp import web
from requests_oauthlib import OAuth2Session
from aiohttp_session import setup, get_session
from dotenv import load_dotenv
import time
import os
import aiohttp_jinja2
import jinja2

load_dotenv()

OAUTH2_CLIENT_ID = os.getenv('CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
OAUTH2_REDIRECT_URI = 'http://localhost:3000/callback'

API_BASE_URL = 'https://discordapp.com/api'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

global session
session = {}

routes = web.RouteTableDef()

class Handler:

    def __init__(self):
        pass

    def success(self, body):
        return web.json_response(body, status=200, content_type='application/json')


@routes.get('/demo')
async def index(request):
    return Handler.success({})


