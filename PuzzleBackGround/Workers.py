#!/usr/bin/python

import gearman
import time
import JobList
import GearmanConfig

class CustomGearmanWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        print "here is on job execute"
        time.sleep(5.0)
        print "this is the first 5.0"
        time.sleep(5.0)
        print "this is the second 5.0"
        return super(CustomGearmanWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    print "here is call back"
    print job.data
    return job.data

newWorker = CustomGearmanWorker([GearmanConfig.gearmanConnection])
newWorker.register_task(JobList.Job_test, task_callback)
newWorker.work()
