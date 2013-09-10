from gearman import GearmanClient
import JobList
import GearmanConfig

def sayHello():
    newClient = GearmanClient([GearmanConfig.gearmanConnection])
    currentRequest = newClient.submit_job(JobList.Job_test, "key1", background=True, wait_until_complete=False)
    newResult = currentRequest.result
    print "here is new result in PuzzleBackGroundCommands:"
    print newResult
    pass
