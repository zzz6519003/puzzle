#encoding=utf8

from config import settings
import web
from iostools.commandLine import *
import json
import urllib
from model import Package as PackageModel
import os

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
            this is the data from POST['data']
            {
                u'category': u'7',
                u'version' : u'5.7',
                u'appName' : u'haozu',
                u'projectPath' : u'/var/www/here',
                u'mailContent' : u'hello world',
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
        print data
        os.system("echo '0%' > " + data['projectPath']+"/progress.log")
        PackageModel.buildPackage(data)
        pass

    def GET(self):
        pass


class InputCommit:
    def POST(self):
        postData = web.input()
        data = json.loads(urllib.unquote(postData['data']))
        return render.inputCommit(data=data)
