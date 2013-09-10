#!/usr/bin/python

import gearman
import time
import JobList
import json

class CustomGearmanWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        print "here is on job execute"
        print currentJob.data
        data = json.loads(currentJob.data)
        print data["key1"]
        return super(CustomGearmanWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    print "here is call back"
    return job.data

