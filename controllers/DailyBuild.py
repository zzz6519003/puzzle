#encoding=utf8
from config import settings
render = settings.render
data = {'pageIndex':'dailyBuild'}


class Index:
    
    def GET(self):

        return render.dailyBuild(data=data);
    