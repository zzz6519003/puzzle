from config import settings
import web
from iostools.commandLine import *
import json
import urllib

db = settings.db

def getPackageInfoForBuild(projectId, category):
    """
        the result of this function is used for user to choose which version need to be build
    """

    data = {}

    #casa = "casa"
    #package(casa)
    #getDependencyArray(casa)
    #getVersionArray(casa, casa)
    #initProject(casa)

    """
        type's definition is:
        0   common node
        1   initial node
        2   offline node
    """

    projectInfo = (db.select('projectList', where="id=" + projectId))[0]

    appId = "%d" % projectInfo['appId']
    appInfo = (db.select('appList', where="id=" + appId))[0]

    data['projectPath'] = projectInfo['projectPath']
    data['appName'] = appInfo['identifier']
    data['version'] = projectInfo['version']
    data['projectId'] = projectId
    data['category'] = category
    data['dependencyArray'] = [{
            'name':'RTNetwork',
            'dependencyId':'1',
            'SHA1Array':[
                {'hash':'12345', 'type':'0', 'isCurrent':'0', 'versionName':'1.0', 'isInit':'0', 'isOffLine':'0'}, 
                {'hash':'23456', 'type':'0', 'isCurrent':'0', 'versionName':'1.1', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'45678', 'type':'0', 'isCurrent':'0', 'versionName':'1.2', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'56789', 'type':'1', 'isCurrent':'0', 'versionName':'2.0', 'isInit':'1', 'isOffLine':'0'},
                {'hash':'67890', 'type':'0', 'isCurrent':'0', 'versionName':'2.1', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'b785ee19d47ee244f67d3d25721615b7808f760a', 'type':'0', 'isCurrent':'1', 'versionName':'2.2', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'89012', 'type':'2', 'isCurrent':'0', 'versionName':'2.3', 'isInit':'0', 'isOffLine':'1'},
                {'hash':'90123', 'type':'0', 'isCurrent':'0', 'versionName':'3.0', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'01234', 'type':'0', 'isCurrent':'0', 'versionName':'4.0', 'isInit':'0', 'isOffLine':'0'}
                ]
        },{
            'name':'RTApiProxy',
            'dependencyId':'2',
            'SHA1Array':[
                {'hash':'12345', 'type':'0', 'isCurrent':'0', 'versionName':'1.0', 'isInit':'0', 'isOffLine':'0'}, 
                {'hash':'23456', 'type':'0', 'isCurrent':'0', 'versionName':'1.1', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'45678', 'type':'0', 'isCurrent':'0', 'versionName':'1.2', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'56789', 'type':'1', 'isCurrent':'0', 'versionName':'2.0', 'isInit':'1', 'isOffLine':'0'},
                {'hash':'67890', 'type':'0', 'isCurrent':'0', 'versionName':'2.1', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'78901', 'type':'0', 'isCurrent':'0', 'versionName':'2.2', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'289cc82d48e8e32e841c8f533af7747d8095f325', 'type':'2', 'isCurrent':'1', 'versionName':'2.3', 'isInit':'0', 'isOffLine':'1'},
                {'hash':'90123', 'type':'0', 'isCurrent':'0', 'versionName':'3.0', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'01234', 'type':'0', 'isCurrent':'0', 'versionName':'4.0', 'isInit':'0', 'isOffLine':'0'}
                ]
            }]
    return data


def buildPackage(packageInfo):
    package(packageInfo)
    return True
