from config import settings
import web
from iostools.commandLine import *
from iostools.tools.ConfigHelper import ConfigHelper
import json
import urllib
from PuzzleBackGround import PuzzleBackGroundCommands

db = settings.db

def getPackageInfoForBuild(projectId, category, type=1):
    """
        the result of this function is used for user to choose which version need to be build

        type's definition is:
        0   common node
        1   initial node
        2   offline node
    """

    data = {}

    projectInfo = (db.select('projectList', where="id=" + projectId))[0]

    appId = "%d" % projectInfo['appId']
    appInfo = (db.select('appList', where="id=" + appId))[0]

    data['projectPath'] = projectInfo['projectPath']
    data['appName'] = appInfo['identifier']
    data['version'] = projectInfo['version']
    data['projectId'] = projectId
    data['category'] = category

    params = {
        'projectId':projectId,
        'projectPath':projectInfo['projectPath'],
        'appName':data['appName'],
        'dependencyType':1,
    }

    result = PuzzleBackGroundCommands.doWork_fetchDependencyInfo(params)

    data['dependencyArray'] = json.loads(result)

    lastPackageInfo = ConfigHelper().initWithProjectPath(params["projectPath"]).getConfigData()

    if lastPackageInfo['category'] != '0':
        for dependencyInfo in lastPackageInfo['dependencyArray']:
            depRepoName = dependencyInfo['repoName']
            depSha1 = dependencyInfo['sha1']
            for depInfo in data['dependencyArray']:
                if depInfo['name'] == depRepoName:
                    for sha1 in depInfo["SHA1Array"]:
                        if sha1['hash'] == depSha1:
                            sha1["isCurrent"] = 1
                        else:
                            sha1["isCurrent"] = 0

    #data['dependencyArray'] = [{
    #        'name':'RTApiProxy',
    #        'dependencyId':'2',
    #        'SHA1Array':[
    #            {'hash':'12345', 'type':'0', 'isCurrent':'0', 'versionName':'1.0', 'isInit':'0', 'isOffLine':'0'},
    #            {'hash':'23456', 'type':'0', 'isCurrent':'0', 'versionName':'1.1', 'isInit':'0', 'isOffLine':'0'},
    #            {'hash':'45678', 'type':'0', 'isCurrent':'0', 'versionName':'1.2', 'isInit':'0', 'isOffLine':'0'},
    #            {'hash':'56789', 'type':'1', 'isCurrent':'0', 'versionName':'2.0', 'isInit':'1', 'isOffLine':'0'},
    #            {'hash':'67890', 'type':'0', 'isCurrent':'0', 'versionName':'2.1', 'isInit':'0', 'isOffLine':'0'},
    #            {'hash':'78901', 'type':'0', 'isCurrent':'0', 'versionName':'2.2', 'isInit':'0', 'isOffLine':'0'},
    #            {'hash':'289cc82d48e8e32e841c8f533af7747d8095f325', 'type':'2', 'isCurrent':'1', 'versionName':'2.3', 'isInit':'0', 'isOffLine':'1'},
    #            {'hash':'90123', 'type':'0', 'isCurrent':'0', 'versionName':'3.0', 'isInit':'0', 'isOffLine':'0'},
    #            {'hash':'01234', 'type':'0', 'isCurrent':'0', 'versionName':'4.0', 'isInit':'0', 'isOffLine':'0'}
    #        ]
    #    }]

    return data


def buildPackage(packageInfo):
    print "buildPackage is here"
    print packageInfo
    PuzzleBackGroundCommands.doWork_packageByPackageInfo(packageInfo)
    return True

def getProjectPath(appId, version):
    appInfo = (db.select('appList', where="id="+appId))[0]
    projectPath = getIosProjectPath(appInfo['identifier'], version)
    return projectPath

def getDependecyInfoArray(dependencyInfo):
    """
        dependencyInfo['projectId']
        dependencyInfo['dependencyId']
        dependencyInfo['dependencyType']
        dependencyInfo['initSHA1'] initSHA1 can be null
        dependencyInfo['numBeforeInitSHA1']
    """
    result = getVersionArray(dependencyInfo)
    return result


