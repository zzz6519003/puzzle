#encoding=utf8

from config import settings
from PuzzleBackGround import PuzzleBackGroundCommands
from iostools.tools.ConfigHelper import ConfigHelper
render = settings.render

class GitCorpDidMergePullRequest:

    def GET(self):
        packageInfo = ConfigHelper().initWithBranchName("develop_p-anjuke_3.1").getConfigData()
        print packageInfo
        pass

