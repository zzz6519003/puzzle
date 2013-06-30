#encoding=utf8
from config import settings
import json
import web
import string
import time
import urllib

render = settings.render
db = settings.db
data = {'pageIndex':'project'}


class Index:
    def GET(self):
        #获取当前日期
        import time
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))
        
        #获取项目列表
        data['projectList'] = db.select('projectList', order="id ASC", _test=False)
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
        #data is{u'eventList': [{u'1': u'2013-06-21'}], u'appId': u'1', u'projectName': u'234'}

        lastInsertedId = db.insert('projectList', projectName=data['projectName'], appId=data['appId'], lastUpdate=time.time(), created=time.time())

        for eventItem in data['eventList']:
            #eventItem is {u'1': u'2013-06-21'}
            category = (eventItem.keys())[0]
            mileStoneTime = time.mktime(time.strptime(eventItem[category], "%Y-%m-%d"))
            db.insert('projectEvent', category=category, projectId=lastInsertedId, name=data['projectName'], startDate=mileStoneTime, endDate='0', created='0', updated='0')
        return
