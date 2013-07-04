#encoding=utf8

from config import settings
import web
from iostools.command_line import *

data = {'pageIndex':'index'}
render = settings.render
db = settings.db

class AjaxCheckNewVersion:
    ''' check whether there is new version available for build '''
    def GET(self):
        pass

    def POST(self):
        pass

class SelectVersions:
    ''' select the app version and its dependicy's version '''
    def GET(self):
        print "here i am"

        casa = "casa"

        package(casa)
        getDependencyArray(casa)
        getVersionArray(casa, casa)
        initProject(casa)

        print web.input()
        return render.selectVersions(data=data)

    def POST(self):
        pass
