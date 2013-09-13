#!/usr/bin/python

from iostools.commandLine import *
import json

def doWork(gearmanWorker, job):
    params = json.loads(job.data)
    print params
    result = getOrganizedDepInfo(params)
    print "\n\n\nresult is:\n%s" % result
    return json.dumps(result)
