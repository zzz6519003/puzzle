#encoding=utf8

from config import settings
import web
from iostools.commandLine import *
import json
import urllib
from model import Package as PackageModel

data = {'pageIndex':'project'}
render = settings.render
db = settings.db

class AjaxCheckNewVersion:
    """ check whether there is new version available for build """
    def GET(self):
        pass

    def POST(self):
        pass


class SelectVersions:
    """ select the app version and its dependency's version """
    def GET(self):
        """
            the page need the name of dependency and SHA1 code array
            and the project ID
            and category

        """

        projectId = (web.input())['projectId']
        category = (web.input())['category']

        data['packageInfoForBuild'] = PackageModel.getPackageInfoForBuild(projectId, category)

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
                array   packageInfo["dependencyArray"]=[dependency, dependency]
                int     packageInfo["category"]
                bool    packageInfo["isDebug"]

            this is the data from POST
            {
                u'category': u'7',
                u'projectId': u'4',
                u'isDebug': True,
                u'dependencyArray': [
                    {
                        u'sha1': u'90123',
                        u'repoId': u'1',
                        u'repoName': u'RTNetwork'
                    },
                    {
                        u'sha1': u'90123',
                        u'repoId': u'2',
                        u'repoName': u'RTApiProxy'
                    }
                ]
            }
        """
        postData = web.input()
        data = json.loads(urllib.unquote(postData['data']));
        PackageModel.package(data)
        pass

    def GET(self):
        pass
