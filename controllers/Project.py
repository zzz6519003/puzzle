#encoding=utf8
from config import settings
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
    