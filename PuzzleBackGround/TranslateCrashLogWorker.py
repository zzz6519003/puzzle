#!/usr/bin/python

import gearman
import time
import JobList
import GearmanConfig

class TranslateCrashLogWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        return super(CustomGearmanWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    return job.data

newWorker = TranslateCrashLogWorker([GearmanConfig.gearmanConnection])
newWorker.register_task(JobList.Job_translate, task_callback)
newWorker.work()
