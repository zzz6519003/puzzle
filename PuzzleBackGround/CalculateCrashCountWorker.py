#!/usr/bin/python

import json

def doWork(gearmanWorker, job):
    print "here i am"
    params = json.loads(job.data)
    print params
    print "\n\n\nresult is:\n%s" % params

