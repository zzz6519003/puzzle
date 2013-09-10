#!/usr/bin/python

import gearman
import time
import JobList
import GearmanConfig

class PackageWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        return super(CustomGearmanWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    return job.data

newWorker = PackageWorker([GearmanConfig.gearmanConnection])
newWorker.register_task(JobList.package, task_callback)
newWorker.work()
