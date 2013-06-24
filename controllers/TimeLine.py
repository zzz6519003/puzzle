#encoding=utf8

from config import settings
import web

data = {'pageIndex':'timeline'}
render = settings.render
db = settings.db

class Index:
    ''' time line class '''
    def GET(self):
        dataGet = web.input()
        appId = dataGet['id']

        data['eventList'] = db.select('projectEvent', order='startDate ASC', where='projectId='+appId)

        return render.timeline(data=data);

    def POST(self):
        pass
