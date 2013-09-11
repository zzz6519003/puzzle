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
    filepath = "/tmp/%s.gearmanjob\n" % job.unique
    fp = open(filepath, "w")
    fp.close()
    return job.data
