#encoding=utf8
db = settings.db
data = {'pageIndex':'appstore'}
from config import settings

render = settings.render

class Index:
    ''' App Store '''
    def GET(self):
        import os,json
        commandLine = "ssh mobile@ios.dev.anjuke.com 'python /var/www/apps/osdirect.py'"
        handle = os.popen(commandLine)
        returnString = handle.readlines()
        data['appList'] = json.loads(returnString[0])
        print data['appList']
        return render.appStoreList(data=data)

    def POST(self):
        pass
