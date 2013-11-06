#!/usr/bin/python
#encoding=utf8
import datetime
import PuzzleBackGroundCommands
now = datetime.datetime.now()
end = now - datetime.timedelta(minutes=30)
end = end.strftime('%Y-%m-%d %H:%M:%S')
PuzzleBackGroundCommands.doWork_calculateCrashCount({'start':'2013-10-28 00:00:00','end':end,'is_old':0})
#PuzzleBackGroundCommands.doWork_warningCrashCount({'start':'2013-10-28 00:00:00','end':end})

