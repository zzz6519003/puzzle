#encoding=utf8

from config import settings
from model import Package
data = {'pageIndex':'home'}
render = settings.render

class Index:
    ''' 主页 '''
    def GET(self):
        data['name'] = "hello"
        return render.index(data=data)

    def POST(self):
        pass
