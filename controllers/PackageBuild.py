#encoding=utf8

from config import settings
import web
from iostools.command_line import *
import json
import urllib

data = {'pageIndex':'index'}
render = settings.render
db = settings.db

class AjaxCheckNewVersion:
    """ check whether there is new version available for build """
    def GET(self):
        pass

    def POST(self):
        pass


class SelectVersions:
    """ select the app version and its dependicy's version """
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


class BuildPackage:
    """ 
        build package by information from post
    """
    def POST(self):
        """
            data is an dictionary.the key is dependencyId
            and the value is the SHA1 code

            dependency is a class which constructed by [id, sha1, repoAddress, name]

            should transfer these params to build a package

                string  packageInfo["projectId"]
                string  packageInfo["appId"]
                string  packageInfo["appSHA1"]
                array   packageInfo["dependencyArray"]=[dependency, dependency]
                int     packageInfo["category"]
                bool    packageInfo["isDebug"]
        """
        postData = web.input()
        data = json.loads(urllib.unquote(postData['data']));
        print data
        pass

    def GET(self):
        pass
