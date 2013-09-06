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
        try:
            mail_to = ["yuetingqian@anjuke.com","vingowang@anjukeinc.com",
                           "clairyin@anjuke.com","angelazhang@anjuke.com"]
            data['result'] = ''
            start = ''
            params = web.input()
            start = params.get('start')
            end = params.get('end')
            is_old = params.get('is_old')
            apps_tmp = puzzle_db.query("SELECT * FROM qa_crashcount_limit")
            app_count = len(apps_tmp)
            end_tmp = datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
            check_start = str(end_tmp-datetime.timedelta(minutes=11))
            check_end = str(end_tmp-datetime.timedelta(minutes=9))
            tmp = puzzle_db.query("SELECT * FROM qa_crashcount WHERE end_time>=$start AND end_time <$end",
                                  vars={'start':check_start,'end':check_end})
            check_count = len(tmp)
            if app_count != check_count:
                dt = str(end_tmp-datetime.timedelta(minutes=10))
                send_mail('['+dt+']crash update fail',dt+'缺少记录','Crash No-Reply',mail_to)
            apps = {}
            for app in apps_tmp:
                id = len(apps)
                apps[id] = {}
                for key in app:
                    apps[id][key] = app[key]

            if not start or not end:
                now = datetime.datetime.now()
                format_now = str(now.strftime('%Y-%m-%d %H:%M:%S'))
                send_mail('[' + format_now + ']缺少同步时间', '缺少同步时间')
                return render.CrashJob(data=data)

            crash = ama_db.query("SELECT c.AppName AS app_name ,c.AppPlatform AS app_platform, "
                                 "count(*) AS count "
                                 "FROM crashdata c "
                                 "LEFT JOIN bs_appid b "
                                 "ON c.AppName = b.AppName AND c.AppPlatform=b.AppPlatform AND c.AppVer = b.AppVer "
                                 "WHERE c.edt < $end AND	c.edt >= $start AND b.isShow = 1 "
                                 "GROUP BY c.AppName,c.AppPlatform", vars={'start': start, 'end': end})
            sub = '[' + end + ']crash report'
            context = ''
            for item in crash:
                res = False
                for i in apps:
                    app = apps[i]
                    if item['app_name'] == app['app_name'] and item['app_platform'] == app['app_platform']:
                        del apps[i]
                        res =True
                        break
                if res == False:
                    continue
                value = {'app_name': item['app_name'], 'app_platform': item['app_platform'],
                         'start_time': start, 'end_time': end}
                crash_count = puzzle_db.select('qa_crashcount',
                                               where="app_name=$app_name AND app_platform =$app_platform "
                                                     " AND start_time =$start_time AND end_time=$end_time", vars=value)
                if len(crash_count) == 0:
                    if not is_old:
                        puzzle_db.insert('qa_crashcount', app_name=item['app_name'], app_platform=item['app_platform'],
                                     crash_count=item['count'], start_time=start, end_time=end)
                    else:
                        puzzle_db.insert('qa_crashcount', app_name=item['app_name'], app_platform=item['app_platform'],
                                     crash_count=item['count'], start_time=start, end_time=end,updated_at=end)
                else:
                    if not is_old:
                        now = datetime.datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        now=end
                    puzzle_db.update('qa_crashcount', where="id=" + str(crash_count[0]['id']),
                                     crash_count=item['count'],
                                     start_time=start, end_time=end, updated_at=now)

                crash_limit = puzzle_db.select('qa_crashcount_limit', where="app_name=$app_name "
                                                                            "AND app_platform =$app_platform ",
                                               vars=value)

                if len(crash_limit) == 1:
                    limit_count = crash_limit[0]['crash_count']
                    if item['count'] > limit_count:
                        context += item['app_name'] + item['app_platform'] + ' crash 实际量为' \
                                   + str(item['count']) + ' , 超过设定值 ' + str(limit_count) + \
                                   ', <a href="http://puzzle.corp.anjuke.com/monitor/detail?app_name='+item['app_name']+\
                                   '&app_platform='+item['app_platform']+'">查看</a><br>'

                else:
                    context += item['app_name'] + item['app_platform'] + '未设置crash数量<br>'
            for i in apps:
                value = {'app_name': apps[i]['app_name'], 'app_platform': apps[i]['app_platform'],
                         'start_time': start, 'end_time': end}
                crash_count = puzzle_db.select('qa_crashcount',
                                               where="app_name=$app_name AND app_platform =$app_platform "
                                                     " AND start_time =$start_time AND end_time=$end_time", vars=value)

                if len(crash_count)==0:
                    if not is_old:
                        puzzle_db.insert('qa_crashcount', app_name=apps[i]['app_name'], app_platform=apps[i]['app_platform'],
                                 crash_count=0, start_time=start, end_time=end)
                    else:
                         puzzle_db.insert('qa_crashcount', app_name=apps[i]['app_name'], app_platform=apps[i]['app_platform'],
                                 crash_count=0, start_time=start, end_time=end,updated_at=end)
                else:

                    if not is_old:
                        now = datetime.datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        now=end
                    puzzle_db.update('qa_crashcount', where="id=" + str(crash_count[0]['id']),
                                     crash_count=0,
                                     start_time=start, end_time=end, updated_at=now)
            if context != '':

                send_mail(sub, context,'Crash No-Reply',mail_to)
            data['result'] = context
            if not is_old:
                apps_tmp = puzzle_db.query("SELECT * FROM qa_crashcount_limit ORDER BY id")
                for item in apps_tmp:
                    file_name = str(item['id'])
                    path = 'static/chart/'
                    file_object = open(path+file_name+'.js', 'w')
                    js = get_chart_js(item['app_name'],item['app_platform'])
                    file_object.write(js)
                    file_object.close()
                    from config import common
                    os.system(common.phantomjs_path+' static/js/highcharts-convert.js '
                              '-infile '+path+file_name+'.js -outfile '+path+file_name+'.png')

        except Exception as err:
            error = '错误信息：' + str(err)
            data['result'] = error
            send_mail('[' + start + ']crash信息更新失败', error,'Crash No-Reply')
        return render.crashJob(data=data)


def get_chart_js(app_name,app_platform,start=None,end=None):

    now = datetime.datetime.now()
    dt_date = now.strftime('%Y-%m-%d')
    if not start or not end:
        dt_date = datetime.datetime.now()
        dt_date = dt_date.strftime('%Y-%m-%d')
        start=dt_date
        end = dt_date
        start = start + ' 00:00:00'
        end = end + ' 23:59:59'
    from controllers.Monitor import get_all_data
    result=get_all_data(app_name,app_platform,start,end)
    js = "\
        Highcharts.theme = {\
            colors: ['#4572a7', '#c0c0c0', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],\
            title: {\
                style: {\
                    color: '#000',\
                    font: 'bold 16px \"Trebuchet MS\", Verdana, sans-serif'\
                }\
            },\
            subtitle: {\
                style: {\
                    color: '#666666',\
                    font: 'bold 12px \"Trebuchet MS\", Verdana, sans-serif'\
                }\
            },\
            legend: {\
                itemStyle: {\
                    font: '9pt Trebuchet MS, Verdana, sans-serif',\
                    color: 'black'\
                },\
                itemHoverStyle: {\
                    color: 'gray'\
                }\
            }\
        };\
        Highcharts.setOptions(Highcharts.theme);\
        var options = {\
            chart: {\
                type: 'spline',\
                renderTo: 'container'\
            },\
            credits: {\
                enabled: false\
            },\
            title: {\
                text: 'Crash Count'\
            },\
            xAxis: {\
                type: 'datetime',\
                dateTimeLabelFormats: { \
                    second: '%H:%M:%S',\
                    minute: '%H:%M',\
                    hour: '%H:%M',\
                    day: '%m-%d',\
                    week: '%m-%d',\
                    month: '%Y-%m',\
                    year: '%Y'\
                }\
            },\
            yAxis: {\
                title: {\
                    text: 'Count'\
                },\
                min: 0\
            },\
            tooltip: {\
                crosshairs: true,\
                formatter: function () {\
                    if (this.series.name == 'lastweek') {\
                        this.x = this.x / 1000 - 7*24*60*60;\
                        this.x = this.x*1000;\
                    }\
                    html = Highcharts.dateFormat('%Y-%m-%d %H:%M', this.x);\
                    html += '<br>' + this.series.name + '：' +\
                        '<span style=\"font-weight:bold;color:' + this.series.color + '\">' +\
                        this.y + '</span>';\
                    return html;\
                },\
                valueSuffix: '个'\
            },\
            plotOptions: {\
                spline: {\
                    lineWidth: 2,\
                    states: {\
                        hover: {\
                            lineWidth: 3\
                        }\
                    },\
                    marker: {\
                        enabled: false,\
                        states: {\
                            hover: {\
                                enabled: true,\
                                radius: 4\
                            }\
                        }\
                    },\
                    pointInterval: 3600000\
                }\
            },\
            series: [\
                {\
                    name: 'today',\
                    data:["
    for i in result[0]:
        utc = get_utc(i[0])

        js +="["+utc+","+str(i[1])+"],"
    js += "]\
                },\
                {\
                    name: 'lastweek',\
                    data:["
    for i in result[1]:
        utc = get_utc(i[0],7)
        js +="["+utc+","+str(i[1])+"],"
    js +="]\
                }\
            ]\
        };\
        Highcharts.setOptions({\
            global: {\
                useUTC: false\
            }\
        });"
    return js

def get_utc(timestamp,days=0):
    utc = str((timestamp+days*24*60*60)*1000)
    return utc