#encoding=utf8

from config import settings
data = {'pageIndex':'home'}
render = settings.render

class Index:
    ''' 主页 '''
    def GET(self):
        data['name'] = "hello"
        import time
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))
        timeStamp = time.localtime(time.time());
        data['currentDay'] = time.strftime('%d',timeStamp);
        data['currentYearAndMonth'] = time.strftime('%Y年%m月',timeStamp);
        return render.index(data=data)

    def POST(self):
        pass
