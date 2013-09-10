from gearman import GearmanClient

def sayHello():
    newClient = GearmanClient(['127.0.0.1:4730'])
    currentRequest = newClient.submit_job("echo", "key1", background=True, wait_until_complete=False)
    newResult = currentRequest.result
    print "here is new result in PuzzleBackGroundCommands:"
    print newResult
    pass
