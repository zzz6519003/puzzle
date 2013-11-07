#encoding=utf8

from config import settings
import web
import json
import urllib
import os

data = {'pageIndex':'index'}
render = settings.render
db = settings.db

class Location:
    def GET(self):
        data['location'] = "孟智在位置上"
        print data
        return render.whereIsMengZhi(data=data)
