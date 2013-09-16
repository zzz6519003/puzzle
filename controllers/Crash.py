#encoding=utf8
import web
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from config import settings
import os
import datetime

from model.GlobalFunc import send_mail

render = settings.render
data = {'pageIndex': 'crash'}
puzzle_db = settings.puzzle_db
ama_db = settings.ama_db


class Set:
    def GET(self):
        params = web.input()
        app_name = params.get('app_name')
        new_app = params.get('new_app')
        if new_app:
            app_name = new_app
        app_platform = params.get('app_platform')
        crash_count = params.get('crash_count')
        if not crash_count:
            crash_count = ''

        if app_name and app_platform and crash_count:
            crash_count = int(crash_count)
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            value = {'app_name': app_name, 'app_platform': app_platform}
            crash_limit = puzzle_db.select('qa_crashcount_limit',
                                           where='app_name=$app_name AND app_platform=$app_platform',
                                           vars=value)
            if len(crash_limit) == 0:
                puzzle_db.insert('qa_crashcount_limit', app_name=app_name, app_platform=app_platform,
                                 crash_count=crash_count, updated_at=now)
            else:
                puzzle_db.update('qa_crashcount_limit', where="id=" + str(crash_limit[0]['id']),
                                 crash_count=crash_count, updated_at=now)

        data['crash_limit'] = puzzle_db.select('qa_crashcount_limit', order="id")
        data['apps'] = puzzle_db.query('SELECT DISTINCT app_name FROM qa_crashcount_limit ORDER BY id')
        data['params'] = {'app_name': app_name, 'app_platform': app_platform, 'crash_count': crash_count}
        return render.crashSet(data=data)


class Job:
    def GET(self):
            job_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mail_to = ["yuetingqian@anjuke.com","vingowang@anjukeinc.com","clairyin@anjuke.com","angelazhang@anjuke.com"]
            mail_to = ["yuetingqian@anjuke.com"]
            data['result'] = ''
            error =''
            start = ''
            params = web.input()
            start = params.get('start')
            end = params.get('end')
            is_old = params.get('is_old')
            from PuzzleBackGround import PuzzleBackGroundCommands
            data['result'] = PuzzleBackGroundCommands.doWork_calculateCrashCount({'start':start,'end':end,'is_old':is_old})
            return render.crashJob(data=data)
