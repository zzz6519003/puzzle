#encoding=utf8

from config import settings
import web
import json
import urllib
import os

data = {'pageIndex':'index'}
render = settings.render
db = settings.dbig import settings

class Location:

    def GET(self):
        render.whereIsMengZhi(data="不在座位上")
        pass
