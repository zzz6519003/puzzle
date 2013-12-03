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
        handler = os.popen("curl 'http://api.dreambuff.com/whereiam/'")
        result = handler.readlines()
        data['location'] = result[0]
        print data
        return render.whereIsMengZhi(data=data)
