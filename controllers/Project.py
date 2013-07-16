#encoding=utf8
from config import settings
import json
import web
import string
import time
import urllib
from iostools.commandLine import *

render = settings.render
db = settings.db
data = {'pageIndex':'project'}


class Index:
    def GET(self):
        #获取当前日期
        import time
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))

        #获取项目列表
        data['projectList'] = db.select('projectList', order="id DESC", _test=False)
        temp = [];
        for item in data['projectList']:
            item['lastUpdate'] = time.strftime('%Y-%m-%d,%H:%M',time.localtime(item['lastUpdate']))
            temp.append(item)
        data['projectList'] = temp

        #获取数据
        return render.projectList(data=data)

class Add:
    def GET(self):

        data['appList'] = db.select('appList', order="id ASC", _test=False)
        temp = [];

        for item in data['appList']:
            item['lastUpdate'] = time.strftime('%Y-%m-%d,%H:%M',time.localtime(item['lastUpdate']))
            temp.append(item)

        data['appList'] = temp

        return render.projectAdd(data=data)

    def POST(self):
        postData = web.input();
        data = json.loads(urllib.unquote(postData['data']));

        print data

        lastInsertedId = db.insert('projectList', projectName=data['projectName'], appId=data['appId'], lastUpdate=time.time(), created=time.time(), version=data['version'], pmtId=data['pmtId'])

        for eventItem in data['eventList']:
            category = (eventItem.keys())[0]
            mileStoneTime = time.mktime(time.strptime(eventItem[category], "%Y-%m-%d"))
            db.insert('projectEvent', category=category, projectId=lastInsertedId, name=data['projectName'], startDate=mileStoneTime, endDate='0', created='0', updated='0')

        #init project
        appInfo = (db.select('appList', where="id="+data['appId']))[0]
        initInfo = {
            'appId':data['appId'],
            'appName':appInfo['identifier'],
            'appRepoUrl':appInfo['appRepo'],

            'projectName':data['projectName'],
            'projectId':lastInsertedId,

            'openXcode':data['openXcode'],
            'IP':web.ctx.ip,
            'whoami':data['whoami'],
            'clientProjectPath':data["clientProjectPath"],
            'version':data['version']
        }

        initProject(initInfo)
        return
