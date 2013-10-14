#encoding=utf8

from config import settings
from PuzzleBackGround import PuzzleBackGroundCommands
render = settings.render

class GitCorpDidMergePullRequest:
    def translater(paramsForTranslate):
        """
            {
                u'category': u'7',   7 is used for Dailybuild, 8 is used for RC build
                u'version' : u'5.7',
                u'appName' : u'haozu',
                u'projectPath' : u'/var/www/here',
                u'mailContent' : u'hello world',
                u'projectId': u'4',
                u'isDebug': True,
                u'versionForPackage': u'5.0.1',
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

    def GET(self):
        print "here i am"
        pass

