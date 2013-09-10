#!/usr/bin/python

#here is on job execute
#<GearmanJob connection/handle=(<GearmanConnection 127.0.0.1:4730 connected=True>, 'H:casas-MacBook-Pro.local:1'), task=echo, unique=f688332cb327829633f5107c11250e46, data='this is the first job'>
#
#here is call back
#this is the first job

import gearman
import time

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

newWorker = CustomGearmanWorker(['127.0.0.1:4730'])
newWorker.register_task("echo", task_callback)
newWorker.work()
