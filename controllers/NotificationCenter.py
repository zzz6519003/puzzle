#encoding=utf8

from config import settings
from PuzzleBackGround import PuzzleBackGroundCommands
from iostools.tools.ConfigHelper import ConfigHelper
from model import Package as PackageModel
import web

"""
package info:
    {
        'category': '7',
        'dependencyArray':
            [
                {'sha1': 'e3aa66', 'repoId': '4', 'repoName': 'RTCoreService'},
                {'sha1': '3a77cc', 'repoId': '5', 'repoName': 'RTNetwork'},
                {'sha1': '66328f', 'repoId': '2', 'repoName': 'RTApiProxy'},
                {'sha1': '4f153d', 'repoId': '6', 'repoName': 'UIComponents'}
            ],
        'channelIdList': [],
        'appName': 'p-anjuke',
        'projectId': '63',
        'isDebug': True,
        'version': '3.1',
        'projectPath': '/var/www/projects/p-anjuke_3.1',
        'webPath': 0,
        'mailContent': ''
    }

"""

class GitCorpDidMergePullRequest:
    def GET(self):
        return "hello world"

    def POST(self):
        postData = web.input()
        print "here is post, %s" % postData
        print "user is %s" % postData["user"]
        print "repo is %s" % postData["repo"]
        print "ref is %s" % postData["ref"]

        """
            user is weiyutian
            repo is weiyutian/shake
            ref is master
        """

        branchName = postData["ref"]
        repo = postData["repo"]

        if "develop" not in branchName:
            return

        packageInfo = ConfigHelper().initWithBranchName(branchName).getConfigData()

        if packageInfo["category"] == '0':
            return

        if packageInfo["category"] != '7' and packageInfo["category"] != '8':
            packageInfo["category"] = '7'

        packageInfo["mailContent"] = "测试puzzle和gitcorp是否能够合并"
        print packageInfo
        PackageModel.buildPackage(packageInfo)
        print "building package"
        pass
