#!/usr/bin/python

import gearman
import time
import JobList
import GearmanConfig
from iostools.commandLine import *
import json

class PuzzlePackageWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        packageInfo = json.loads(currentJob.data)
        package(packageInfo)
        return super(PuzzlePackageWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    return job.data
