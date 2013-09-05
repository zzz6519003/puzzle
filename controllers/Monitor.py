#encoding=utf8
import web
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from config import settings
import time
import datetime
import json
from model.GlobalFunc import send_mail

render = settings.render
data = {'pageIndex': 'Monitor'}
puzzle_db = settings.puzzle_db
ama_db = settings.ama_db


class ChartList:
    def GET(self):
        apps_tmp = puzzle_db.query("SELECT * FROM qa_crashcount_limit WHERE is_show=1 ORDER BY id")
        apps = {}
        for app in apps_tmp:
            apps[app['id']] = app
        dt_date = datetime.datetime.now()
        dt_date = dt_date.strftime('%Y-%m-%d')
        data['dt_date'] = dt_date

        data['apps'] = apps


        return render.monitorChartList(data=data)


class Detail:
    def GET(self):
        params = web.input()
        app_name = params.get('app_name')
        if app_name:
            data['app_name'] = app_name
        else:
            data['app_name'] = ''
        app_platform = params.get('app_platform')
        if app_platform:
            data['app_platform'] = app_platform
        else:
            data['app_platform'] = ''
        now = datetime.datetime.now()
        dt_date = now.strftime('%Y-%m-%d')
        data['dt_date'] = dt_date
        yesterday = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        three = (now -datetime.timedelta(days=3)).strftime('%Y-%m-%d')
        seven = (now -datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        fifteen =(now -datetime.timedelta(days=15)).strftime('%Y-%m-%d')
        thirty = (now -datetime.timedelta(days=30)).strftime('%Y-%m-%d')

        data['yesterday'] = yesterday
        data['three'] = three
        data['seven'] = seven
        data['fifteen'] = fifteen
        data['thirty'] = thirty

        return render.monitorDetail(data=data)


class GetData:
    def GET(self):
        params = web.input()
        app_name = params.get('app_name')
        app_platform = params.get('app_platform')
        start = params.get('start')
        end = params.get('end')
        print app_name,app_platform,start,end
        if not app_name or not app_platform or not start or not end:
            data['result']=[]
            return render.monitorGetData(data=data)

        start = start + ' 00:00:00'
        end = end + ' 23:59:59'

        if app_name and app_platform and start and end:

            result = get_all_data(app_name,app_platform,start,end)

            data['result'] = json.dumps(result)

        return render.monitorGetData(data=data)


def get_data(value):
    crashs = puzzle_db.select('qa_crashcount',
                              where="app_name=$app_name AND app_platform=$app_platform "
                                    "AND end_time >=$start AND end_time < $end ORDER BY end_time",
                              vars=value
    )
    result = []
    for item in crashs:
        time_tmp=str(item['end_time'])[:-3]
        dt = datetime.datetime.strptime(time_tmp, '%Y-%m-%d %H:%M')
        list = [int(time.mktime(dt.timetuple()))]
        list.append(int(item['crash_count']))
        result.append(list)
    return result

def get_all_data(app_name,app_platform,start,end):
    lastweek = 1;
    value = {'app_name': app_name, 'app_platform': app_platform, 'start': start, 'end': end}
    result = []
    today = get_data(value)

    pre_end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    pre_end = str(pre_end - datetime.timedelta(days=lastweek))

    pre_start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    pre_start = str(pre_start - datetime.timedelta(days=lastweek))
    value = {'app_name': app_name, 'app_platform': app_platform, 'start': pre_start, 'end': pre_end}
    pre_week = get_data(value)
    result.append(today)
    result.append(pre_week)
    return result

