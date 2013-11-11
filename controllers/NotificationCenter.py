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
            user is mobile
            repo is mobile/ios_AnjukeHD
            ref is master
        """

        branchName = postData["ref"]
        repoInfo = postData["repo"].split("/")
        repoName = repoInfo[1]
        user = postData["user"]

        if user == "wadecong":
            print "user is wadecong, do nothing"
            return

        if "develop" not in branchName:
            print "this is not develop, do nothing"
            return

        packageInfo = ConfigHelper().initWithBranchName(branchName).getConfigData()

        if packageInfo["category"] == '0':
            return

        if packageInfo["category"] != '7' and packageInfo["category"] != '8':
            packageInfo["category"] = '7'

        packageInfo["mailContent"] = "puzzle自动打包."
        print packageInfo
        PackageModel.buildPackage(packageInfo)
        print "notification building package"
        pass
