#!/usr/bin/python

import gearman
import time
import JobList
import GearmanConfig

class PuzzlePackageWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        return super(PuzzlePackageWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    return job.data
