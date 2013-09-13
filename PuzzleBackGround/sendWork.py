#!/usr/bin/python


params = {
    'projectId':'37',
    'projectPath':'/var/www/projects/i-anjuke_4.0',
    'appName':'i-anjuke',
    'dependencyType':1,
}

#import PuzzleBackGroundCommands
#PuzzleBackGroundCommands.doWork_getDependencyInfo(params)

from PuzzleBackGroundCommands import *
import json

client = GearmanClient([GearmanConfig.gearmanConnection])
data = json.dumps(params)
request = client.submit_job(JobList.Job_getDependencyInfo, data, wait_until_complete=True)
print request
print request.result
