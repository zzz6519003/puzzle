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
        GET_data = web.input()
        print GET_data

        if not GET_data.has_key("appId"):
            appId = "1"
        else:
            appId = GET_data['appId']

        shouldDelete = GET_data.has_key("delete")
        print "here i am"
        print "here i am"
        print "here i am"
        print "here i am"
        print shouldDelete

        #获取当前日期
        import time
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))
        timeStamp = time.localtime(time.time());
        data['currentDay'] = time.strftime('%d',timeStamp);
        data['currentYearAndMonth'] = time.strftime('%Y年%m月',timeStamp);
        #获取项目列表
        data['projectList'] = db.select('projectList', order="id DESC", where="appId="+appId, _test=False)
        temp = [];
        for item in data['projectList']:
            item['lastUpdate'] = time.strftime('%Y-%m-%d,%H:%M',time.localtime(item['lastUpdate']))
            temp.append(item)

        appList = db.select('appList').list()
        data['appMain'] = []
        data['appMain'].append(appList.pop(0))
        data['appMain'].append(appList.pop(4))
        data['appMain'].append(appList.pop(6))
        print data['appMain']
        data['projectList'] = temp
        data['currentAppId'] = appId
        data['appList'] = appList

        #获取数据
        if shouldDelete:
            return render.deleteProjectList(data=data)
        else:
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

            'openXcode':False,
            'IP':web.ctx.ip,
            'whoami':data['whoami'],
            'clientProjectPath':data["clientProjectPath"],
            'version':data['version']
        }

        initProject(initInfo)
        return

class Del:
    def POST(self):
        postData = web.input();
        print postData
        pass

class InitScript:
    def GET(self):
        data = web.input()
        print "here is init script"
        print data

        appInfo = (db.select('appList', where="id="+data['appId']))[0]

        projectPath = getIosProjectPath(appInfo['identifier'], data['version'])
        print "project path is " + projectPath

        initScriptPath = projectPath + '/init.py'
        print "init script path is " + initScriptPath

        fileContent = ""

        initScript = open(initScriptPath)
        for line in initScript:
            fileContent = fileContent + "<p>" + line + "</p>"

        return render.initScriptContent(data=fileContent)
