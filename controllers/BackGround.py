#encoding=utf8

from config import settings
from PuzzleBackGround import PuzzleBackGroundCommands
render = setting.render

class StartGearman:
    def GET(self):
        PuzzleBackGroundCommands.sayHello()
        pass

class GearmanStatus:
    def GET(self):
        print "gearman status"
        print PuzzleBackGroundCommands.getStatus()
        pass

class GearmanWorkers:
    def GET(self):
        print "gearman workers"
        print PuzzleBackGroundCommands.getWorkers()
        pass

class RestartWorkers:
    def GET(self):
        return render.background(data=data)

