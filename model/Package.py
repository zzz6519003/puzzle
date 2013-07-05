from config import settings 
import web
from iostools.commandLine import *
import json
import urllib

db = settings.db

def getPackageInfoForBuild(projectId, category):

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
                {'hash':'78901', 'type':'0', 'isCurrent':'1', 'versionName':'2.2', 'isInit':'0', 'isOffLine':'0'},
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
                {'hash':'89012', 'type':'2', 'isCurrent':'1', 'versionName':'2.3', 'isInit':'0', 'isOffLine':'1'},
                {'hash':'90123', 'type':'0', 'isCurrent':'0', 'versionName':'3.0', 'isInit':'0', 'isOffLine':'0'},
                {'hash':'01234', 'type':'0', 'isCurrent':'0', 'versionName':'4.0', 'isInit':'0', 'isOffLine':'0'}
                ]
            }]
    return data
