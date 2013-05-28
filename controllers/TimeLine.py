#encoding=utf8

from config import settings
data = {'pageIndex':'timeline'}
render = settings.render

class Index:
    ''' time line class '''
    def GET(self):
        data['name'] = "hello"
        return render.timeline(data=data);

    def POST(self):
        pass
