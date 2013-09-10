#encoding=utf8

from gearman import GearmanClient, GearmanAdminClient, DataEncoder
import JobList
import GearmanConfig
import json
import os
import time

CreateProjectWorkerPidFilePath      =  "/tmp/CreateProjectWorkerPid"
PackageWorkerPidFilePath            =  "/tmp/PackageWorkerPid"
TranslateCrashLogWorkerPidFilePath  =  "/tmp/TranslateWorkerPid"

class PickleDataEncoder(DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)

class PuzzleGearmanClient(GearmanClient):
    data_encoder = PickleDataEncoder

#test
def sayHello():
    data = {"key1":"value1", "key2":"value2"}
    newClient = PuzzleGearmanClient([GearmanConfig.gearmanConnection])
    currentRequest = newClient.submit_job(JobList.Job_createProject, data, wait_until_complete=False)
    newResult = currentRequest.result
    print "here is new result in PuzzleBackGroundCommands:"
    print currentRequest
    pass

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
    pass

def stopAllWorkers():
    stopCreateProjectWorkers()
    stopPackageWorkers()
    stopTranslateCrashLogWorkers()
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
