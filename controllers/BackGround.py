#encoding=utf8

from config import settings
from PuzzleBackGround import PuzzleBackGroundCommands

class StartGearman:
    def GET(self):
        PuzzleBackGroundCommands.sayHello()
        pass

    def POST(self):
        pass
