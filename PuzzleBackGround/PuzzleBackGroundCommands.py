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
    currentRequest = newClient.submit_job(JobList.Job_test, data, wait_until_complete=False)
    newResult = currentRequest.result
    print "here is new result in PuzzleBackGroundCommands:"
    print currentRequest
    pass

def test():
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
        os.system("kill%s" % pidString)
        os.remove(pidFilePath)
    pass

def startCreateProjectWorkers():
    import CreateProjectWorker
    from CreateProjectWorker import PuzzleCreateProjectWorker

    stopCreateProjectWorkers()

    for i in range(0, 1):
        time.sleep(1)
        result = os.fork()
        if result == 0:
            workerPid = os.getpid()
            print workerPid
            fp = open(CreateProjectWorkerPidFilePath, "a")
            fp.write(" %s" % workerPid)
            fp.close()

            worker = PuzzleCreateProjectWorker([GearmanConfig.gearmanConnection])
            worker.register_task(JobList.Job_test, Workers.task_callback)
            worker.work()
    pass

def startPackageWorkers():
    pass

def startTranslateCrashLogWorkers():
    pass

def stopCreateProjectWorkers():
    killWorkersByPidFile(CreateProjectWorkerPidFilePath)
    pass

def stopPackageWorkers():
    killWorkersByPidFile(PackageWorkerPidFilePath)
    pass

def stopTranslateCrashLogWorkers():
    killWorkersByPidFile(TranslateCrashLogWorkerPidFilePath)
    pass
