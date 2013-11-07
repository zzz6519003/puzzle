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
        crash_count = params.get('crash_count','')

        if app_name and app_platform and crash_count != '':
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
            data['result'] = '缺少参数'
            error =''
            start = ''
            params = web.input()
            start = params.get('start')
            end = params.get('end')
            is_old = params.get('is_old')
            if end:
                from PuzzleBackGround import PuzzleBackGroundCommands
                data['result'] = PuzzleBackGroundCommands.doWork_calculateCrashCount({'start':start,'end':end,'is_old':is_old})
            return render.crashJob(data=data)

class SetTitle:
    def GET(self):
        params = web.input()
        app_name = params.get('app_name')
        app_platform = params.get('app_platform')
        crash_count = params.get('crash_count','')
        crash_title = params.get('crash_title','')
        is_del = params.get('is_del')
        title_id = params.get('title_id')

        if is_del and id:
            puzzle_db.delete('qa_crashtitle',where="id=$title_id",vars={'title_id': title_id})


        data['apps'] = puzzle_db.query("SELECT DISTINCT app_name FROM qa_crashcount_limit ORDER BY id")
        if app_name and app_platform and crash_count !='' and crash_title != '':
            value = {
                    'app_name': app_name,
                    'app_platform': app_platform,
                    'crash_title': crash_title
                    }
            db_crash_title = puzzle_db.query(
                                    "SELECT t.id, app_name, app_platform, crash_title, t.crash_count \
                                    FROM qa_crashcount_limit l, qa_crashtitle t \
                                    WHERE l.id = t.app_id AND app_name = $app_name AND app_platform = $app_platform \
                                    AND crash_title = $crash_title", vars = value
                                    )
            if len(db_crash_title) > 0:
                value['title_id'] = db_crash_title[0]['id']
                puzzle_db.update('qa_crashtitle', where="id=$title_id",
                        vars=value, crash_title=crash_title, crash_count=crash_count,
                        updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
            else:
                app = puzzle_db.select('qa_crashcount_limit', where="app_name=$app_name AND app_platform=$app_platform", vars=value)
                if len(app) > 0:
                    puzzle_db.insert('qa_crashtitle', app_id=app[0]['id'], crash_title=crash_title,crash_count=crash_count)
        data['params'] = {'app_name': app_name, 'app_platform': app_platform, 'crash_count': crash_count, 'crash_title': crash_title}
        data['crash_titles'] = puzzle_db.query(
                                        "SELECT t.id, app_name, app_platform, crash_title, t.crash_count \
                                        FROM qa_crashcount_limit l, qa_crashtitle t \
                                        WHERE l.id = t.app_id"
                                        )


        return render.crashSetTitle(data=data)
