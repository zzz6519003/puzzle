from config import settings
import web
from iostools.commandLine import *
import json
import urllib

db = settings.db

def getPackageInfoForBuild(projectId, category, type=1):
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

    params = {
        'projectId':projectId,
        'projectPath':projectInfo['projectPath'],
        'appName':data['appName'],
        'dependencyType':1,
    }

    data['dependencyArray'] = getOrganizedDepInfo(params)

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
    package(packageInfo)
    sendmailToQA(packageInfo)
    return True


def sendmailToQA(packageInfo):
    from turbomail import Message, interface

    print "sending email"
    print "here is packageInfo"
    print packageInfo
    print "packageInfo done"

    try:
        mail_config = {
            'mail.on':True,
            'mail.manager' : 'immediate',
            'mail.transport' : 'smtp',
            'mail.smtp.server' : '10.10.6.209'
        }
        interface.start(mail_config)

        mail = Message()
        mail.subject = "hello world"
        mail.sender = "noreply@dm.anjuke.com"
        mail.to = "weiyutian@anjuke.com , wadecong@anjuke.com"
        mail.encoding = "utf-8"
        mail.plain = packageInfo['mailContent']
        #mail.plain = "here"
        #mail.author = "casa"
        mail.send()
    except Exception, e:
        print e
    print "success"
    pass


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
