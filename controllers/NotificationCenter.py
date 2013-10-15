#encoding=utf8

from config import settings
from PuzzleBackGround import PuzzleBackGroundCommands
from iostools.tools.ConfigHelper import ConfigHelper
render = settings.render

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
        packageInfo = ConfigHelper().initWithBranchName("develop_p-anjuke_3.1").getConfigData()
        print packageInfo
        pass

