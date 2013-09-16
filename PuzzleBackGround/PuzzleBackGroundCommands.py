#encoding=utf8

from gearman import GearmanClient, GearmanAdminClient, GearmanWorker
import JobList
import GearmanConfig
import json
import os
import time

CreateProjectWorkerPidFilePath        =  "/tmp/CreateProjectWorkerPid"
PackageWorkerPidFilePath              =  "/tmp/PackageWorkerPid"
TranslateCrashLogWorkerPidFilePath    =  "/tmp/TranslateWorkerPid"
FetchDependencyInfoWorkerPidFilePath  =  "/tmp/FetchDependencyInfoWorkerPid"
CaculateCrashCountPidFilePath         =  "/tmp/CaculateCrashCountWorkerPid"

#do work
def doWork_packageByPackageInfo(packageInfo):
    client = GearmanClient([GearmanConfig.gearmanConnection])
    data = json.dumps(packageInfo)
    request = client.submit_job(JobList.Job_package, data, wait_until_complete=False)
    pass

def doWork_fetchDependencyInfo(params):
    """
        params = {
            'projectId':projectId,
            'projectPath':projectInfo['projectPath'],
            'appName':data['appName'],
            'dependencyType':1,
        }
    """
    client = GearmanClient([GearmanConfig.gearmanConnection])
    data = json.dumps(params)
    request = client.submit_job(JobList.Job_fetchDependencyInfo, data, wait_until_complete=True)
    return request.result
    pass

def doWork_calculateCrashCount(params):
    client = GearmanClient([GearmanConfig.gearmanConnection])
    data = json.dumps(params)
    request = client.submit_job(JobList.Job_calculateCrashCount, data,wait_until_complete=True)
    return request.result

#status functions
def getStatus():
    adminClient = GearmanAdminClient([GearmanConfig.gearmanConnection])
    return adminClient.get_status()

def getWorkers():
    adminClient = GearmanAdminClient([GearmanConfig.gearmanConnection])
    return adminClient.get_workers()

#workers life circle
def restartAllWorkers():
    startAllWorkers()
    pass

def startAllWorkers():
    startCreateProjectWorkers()
    startPackageWorkers()
    startTranslateCrashLogWorkers()
    startFetchDependencyInfoWorkers()
    startCalculateCrashCountWorkers()
    pass

def stopAllWorkers():
    stopCreateProjectWorkers()
    stopPackageWorkers()
    stopTranslateCrashLogWorkers()
    stopFetchDependencyInfoWorker()
    stopCalculateCrashCountWorkers()
    pass


def getWorkerPids(pidFilePath):
    if(os.path.isfile(pidFilePath)):
        fp = open(pidFilePath, "r")
        pidString = fp.read()
        return pidString
    else:
        return ""

def killWorkersByPidFile(pidFilePath):
    pidString = getWorkerPids(pidFilePath)
    if (pidString != ""):
        #这个命令不需要空格，因为储存pid的时候前面已经加了空格了
        print "file path is %s" % pidFilePath
        print "kill%s" % pidString
        os.system("kill%s" % pidString)
        os.remove(pidFilePath)
    else:
        print "no need to kill any pid"

def startCreateProjectWorkers():
    import CreateProjectWorker
    from CreateProjectWorker import PuzzleCreateProjectWorker

    stopCreateProjectWorkers()

    for i in range(0, 1):

        time.sleep(1)
        result = os.fork()

        if result == 0:
            workerPid = os.getpid()

            fp = open(CreateProjectWorkerPidFilePath, "a")
            fp.write(" %s" % workerPid)
            fp.close()

            print "ceate project worker started, pid# %s" % workerPid
            print "task name is %s" % JobList.Job_createProject

            worker = PuzzleCreateProjectWorker([GearmanConfig.gearmanConnection])
            worker.register_task(JobList.Job_createProject, CreateProjectWorker.task_callback)
            worker.work()
    pass

def startPackageWorkers():
    import PackageWorker
    from PackageWorker import PuzzlePackageWorker

    stopPackageWorkers()

    for i in range(0, 1):

        time.sleep(1)
        result = os.fork()

        if result == 0:
            workerPid = os.getpid()

            fp = open(PackageWorkerPidFilePath, "a")
            fp.write(" %s" % workerPid)
            fp.close()

            print "ceate project worker started, pid# %s" % workerPid
            print "task name is %s" % JobList.Job_package

            worker = PuzzlePackageWorker([GearmanConfig.gearmanConnection])
            worker.register_task(JobList.Job_package, PackageWorker.task_callback)
            worker.work()
    pass

def startTranslateCrashLogWorkers():
    import TranslateCrashLogWorker
    from TranslateCrashLogWorker import PuzzleTranslateCrashLogWorker

    stopTranslateCrashLogWorkers()

    for i in range(0, 1):

        time.sleep(1)
        result = os.fork()

        if result == 0:
            workerPid = os.getpid()

            fp = open(TranslateCrashLogWorkerPidFilePath, "a")
            fp.write(" %s" % workerPid)
            fp.close()

            print "ceate project worker started, pid# %s" % workerPid
            print "task name is %s" % JobList.Job_translate

            worker = PuzzleTranslateCrashLogWorker([GearmanConfig.gearmanConnection])
            worker.register_task(JobList.Job_translate, TranslateCrashLogWorker.task_callback)
            worker.work()
    pass

def startFetchDependencyInfoWorkers():
    import FetchDependencyInfoWorker

    stopFetchDependencyInfoWorker()

    for i in range(0, 1):
        time.sleep(1)
        result = os.fork()

        if result == 0:
            workerPid = os.getpid()

            fp = open(FetchDependencyInfoWorkerPidFilePath, "a")
            fp.write(" %s" % workerPid)
            fp.close()

            worker = GearmanWorker([GearmanConfig.gearmanConnection])
            worker.register_task(JobList.Job_fetchDependencyInfo, FetchDependencyInfoWorker.doWork)
            worker.work()
    pass

def startCalculateCrashCountWorkers():
    import CalculateCrashCountWorker
    stopCalculateCrashCountWorkers()
    result = os.fork()

    if result == 0:
        workerPid = os.getpid()

        #fp = open(CaculateCrashCountPidFilePath, "a")
        #fp.write(" %s" % workerPid)
        #fp.close()

        print "caculate crash job  worker started, pid# %s" % workerPid
        print "task name is %s" % JobList.Job_calculateCrashCount

        worker = GearmanWorker([GearmanConfig.gearmanConnection])
        worker.register_task(JobList.Job_calculateCrashCount, CalculateCrashCountWorker.doWork)
        worker.work()
    pass





def stopFetchDependencyInfoWorker():
    print "stopping fetch dependency info worker"
    killWorkersByPidFile(FetchDependencyInfoWorkerPidFilePath)
    pass


def stopCreateProjectWorkers():
    print "stopping create project worker"
    killWorkersByPidFile(CreateProjectWorkerPidFilePath)
    pass

def stopPackageWorkers():
    print "stopping package worker"
    killWorkersByPidFile(PackageWorkerPidFilePath)
    pass

def stopTranslateCrashLogWorkers():
    print "stopping translate worker"
    killWorkersByPidFile(TranslateCrashLogWorkerPidFilePath)
    pass

def stopCalculateCrashCountWorkers():
    print "stopping caculate crash count worker"
    killWorkersByPidFile(CaculateCrashCountPidFilePath)
    pass
