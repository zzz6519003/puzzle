#encoding=utf8

from config import settings
import web
import time
import os
import json
import urllib
from model import Package as PackageModel

data = {'pageIndex':'project'}
render = settings.render
db = settings.db


class ShowCmdLog:
    def GET(self):
    # These headers make it work in browsers
        data = web.input()
        #print data
        #   'category': u'7',
        #   'appName': u'i-haozu2.0',
        #   'projectPath': u'/var/www/projects/i-haozu2.0_5.7',
        #   'version': u'5.7',
        #   'projectId': u'33',
        #   'type': u'dailybuild' or u'rc'

        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')

        filePath = data['projectPath'] + "/output.log"
        jsScrollDown = "<script type=\"text/javascript\">document.body.scrollTop = document.body.scrollHeight</script>"

        os.system("echo '' > "+filePath)
        #os.system("touch "+filePath)

        f = open(filePath)

        for line in f:
            yield "<p>"+line+"</p>"+jsScrollDown

        while 1:
            location = f.tell()
            line = f.readline()
            if line:
                if line.find("EOF") != -1:
                    yield "<p>finish</p>"+jsScrollDown
                    return
                else:
                    yield "<p>"+line+"</p>"+jsScrollDown
            else:
                f.seek(location)



class ProgressNumber:
    def GET(self):
        data = web.input()
        #print data
        #   'category': u'7',
        #   'appName': u'i-haozu2.0',
        #   'projectPath': u'/var/www/projects/i-haozu2.0_5.7',
        #   'version': u'5.7',
        #   'projectId': u'33',
        #   'type': u'dailybuild' or u'rc'

        filePath = data['projectPath']+"/progress.log"
        os.system("touch " + filePath)
        progress = open(filePath).readline()
        return progress

class InitProjectProgressBar:
    def POST(self):
        postData = web.input()
        data = json.loads(urllib.unquote(postData['data']));
        print data
        projectPath = PackageModel.getProjectPath(data['appId'], data['version'])
        filePath = projectPath + "/init_progress.log"
        os.system("touch " + filePath)
        progress = open(filePath).readline()
        return progress
