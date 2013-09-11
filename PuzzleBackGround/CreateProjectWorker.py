#!/usr/bin/python

import gearman
import time
import JobList
import GearmanConfig
import os

class PuzzleCreateProjectWorker(gearman.GearmanWorker):
    def on_job_execute(self, currentJob):
        return super(PuzzleCreateProjectWorker, self).on_job_execute(currentJob)


def task_callback(gearmanWorker, job):
    return job.data
