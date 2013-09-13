#!/usr/bin/python
from PuzzleBackGroundCommands import *

import FetchDependencyInfoWorker
import gearman

worker = gearman.GearmanWorker([GearmanConfig.gearmanConnection])
worker.register_task(JobList.Job_fetchDependencyInfo, FetchDependencyInfoWorker.doWork)
worker.work()
