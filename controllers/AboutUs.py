
#encoding=utf8

from config import settings

render = settings.render

class AboutUs:
    ''' 关于我们 '''
    def GET(self):
        return render.index("about us")

    def POST(self):
        pass
