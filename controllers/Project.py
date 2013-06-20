#encoding=utf8
from config import settings
import json
import web
import string
import time

render = settings.render
db = settings.db
data = {'pageIndex':'project'}


class Index:
    def GET(self):
        #获取当前日期
        import time
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()));
        
        #获取项目列表
        data['projectList'] = db.select('projectList', order="id ASC", _test=False);
        temp = [];
        for item in data['projectList']:
            item['lastUpdate'] = time.strftime('%Y-%m-%d,%H:%M',time.localtime(item['lastUpdate']));
            temp.append(item);
        data['projectList'] = temp;
        #获取数据
        return render.projectList(data=data);
    
class Add:
    def GET(self):
        return render.projectAdd(data=data);

    def POST(self):
        data = web.input()

        #squenceId = db.insert('projectEvent', category="1", projectId='2', startDate='3', endDate='4', created='5', updated='6')
        #print squenceId

        projectId = '1'
        projectName = 'casaProject'

        for index in range(1,11):
            attr = "%d" % index
            if hasattr(data, attr):
                mileStoneTime = time.mktime(time.strptime(data[attr], "%Y-%m-%d"))
                db.insert('projectEvent', category=attr, projectId=projectId, startDate=mileStoneTime, endDate='0', created='0', updated='0')























