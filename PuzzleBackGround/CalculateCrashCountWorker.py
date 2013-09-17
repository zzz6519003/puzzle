#!/usr/bin/python
#encoding=utf8
import json
import sys
import web
reload(sys)
sys.setdefaultencoding('utf8')
import os
import datetime
sys.path.append("../config")
import common
import settings
import time
sys.path.append("../model")
from GlobalFunc import send_mail
puzzle_db = settings.puzzle_db
ama_db = settings.ama_db
data={}

def doWork(gearmanWorker, job):
    params = json.loads(job.data)
    job_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mail_to = ["yuetingqian@anjuke.com"]
    data['result'] = ''
    error = ''
    start = params['start']
    end_tmp = params['end']
    is_old = params['is_old']
    result = ''
    db_end_obj = puzzle_db.query("SELECT end FROM qa_jobtime WHERE end <=$end ORDER BY end DESC LIMIT 1",
            vars={'end':end_tmp})
    date_end = datetime.datetime.strptime(end_tmp,'%Y-%m-%d %H:%M:%S')
    timestamp = time.mktime(date_end.timetuple())
    ten_count = int(timestamp/600)
    if len(db_end_obj)==0:
        tmp = (ten_count-1)*600
        db_end = datetime.datetime.fromtimestamp(tmp)
    else:
        db_end = db_end_obj[0]['end']
    db_end = datetime.datetime.strptime(str(db_end),'%Y-%m-%d %H:%M:%S')
    diff_time = (date_end - db_end).seconds

    if diff_time <1200:
        count = 1
    else:
        count = int(diff_time/600)
    i = 0
    lack_context = ''
    start_tmp = db_end + datetime.timedelta(seconds=1)
    end_tmp = db_end + datetime.timedelta(seconds=600)
    for i in range(0,count):
        try:
            start = str(start_tmp)
            end = str(end_tmp)

            if i !=(count-1):
                lack_context += start+'至'+end+'缺少记录<br>'
            apps_tmp = puzzle_db.query("SELECT * FROM qa_crashcount_limit")
            apps = {}
            for app in apps_tmp:
                id = len(apps)
                apps[id] = {}
                for key in app:
                    apps[id][key] = app[key]


            crash = ama_db.query("SELECT c.AppName AS app_name ,c.AppPlatform AS app_platform, \
                                     count(*) AS count \
                                     FROM (SELECT DISTINCT CrashTitle,CrashDetail,AppPlatform, \
                                     AppName,AppVer,DeviceID,NewID,CrashTime \
	        		                 FROM crashdata  \
                                     WHERE edt < $end AND	edt >= $start ) c \
                                     LEFT JOIN bs_appid b \
                                     ON c.AppName = b.AppName AND c.AppPlatform=b.AppPlatform AND c.AppVer = b.AppVer \
                                     WHERE  b.isShow = 1 \
                                     GROUP BY c.AppName,c.AppPlatform", vars={'start': start, 'end': end})
            sub = '非常重要[' + end + ']crash report'
            context = ''
            for item in crash:
                res = False
                for i in apps:
                    app = apps[i]
                    if item['app_name'] == app['app_name'] and item['app_platform'] == app['app_platform']:
                        del apps[i]
                        res = True
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
                                         crash_count=item['count'], start_time=start, end_time=end, updated_at=end)
                else:
                    if not is_old:
                        now = datetime.datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        now = end
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
                                   ', <a href="http://puzzle.corp.anjuke.com/monitor/detail?app_name=' + item['app_name'] + \
                                   '&app_platform=' + item['app_platform'] + '">查看</a><br>'
                        crash_context = ama_db.query("SELECT DISTINCT c.CrashTitle AS title,c.AppVer AS ver,"
                                                     "c.DeviceID AS DeviceID,c.NewID AS NewId,c.CrashTime AS crashTime "
                                                     "FROM crashdata c "
                                                     "LEFT JOIN bs_appid b "
                                                     "ON c.AppName = b.AppName AND c.AppPlatform=b.AppPlatform AND c.AppVer = b.AppVer "
                                                     "WHERE c.edt < $end AND	c.edt >= $start AND b.isShow = 1 "
                                                     "AND c.AppName = $app_name AND c.AppPlatform=$app_platform",
                                                     vars={'start': start, 'end': end, 'app_name': item['app_name'],
                                                           'app_platform': item['app_platform']})
                        style = 'style="font-size:13px;font-family:Arial;background:#F7F7F0;border:1px solid #D7D7D7;' \
                                'border-collapse: collapse;font-weight:bold;padding:2px 8px;vertical-align:bottom;' \
                                'white-space:nowrap;border-image:initial;text-align:left;"'
                        context += '<table style="TABLE-LAYOUT: fixed;; WORD-BREAK: break-all;;border-collapse: collapse">'
                        context += '<tr><td ' + style + '>id</td><td ' + style + '>app</td><td ' + style + '>os</td>' \
                                                                                                           '<td ' + style + '>version</td><td  ' + style + ' width="10%">title</td><td  ' + style + '>time</td></tr>'
                        i = 1

                        for detail in crash_context:
                            context += '<tr><td ' + style + '>' + str(i) + '</td><td ' + style + '>' + item['app_name'] + \
                                       '</td><td ' + style + '>' + item[
                                           'app_platform'] + '</td ' + style + '><td ' + style + '>' \
                                       + detail['ver'] + '</td><td ' + style + ' nowrap>' + detail[
                                           'title'] + '</td><td ' + style + '>' \
                                       + str(detail['crashTime']) + '</td></tr>'
                            i = i + 1

                        context += '</table><br>'

                else:
                    context += item['app_name'] + item['app_platform'] + '未设置crash数量<br>'
            for i in apps:
                value = {'app_name': apps[i]['app_name'], 'app_platform': apps[i]['app_platform'],
                         'start_time': start, 'end_time': end}
                crash_count = puzzle_db.select('qa_crashcount',
                                               where="app_name=$app_name AND app_platform =$app_platform "
                                                     " AND start_time =$start_time AND end_time=$end_time", vars=value)
                if len(crash_count) == 0:
                    if not is_old:
                        puzzle_db.insert('qa_crashcount', app_name=apps[i]['app_name'],
                                         app_platform=apps[i]['app_platform'],
                                         crash_count=0, start_time=start, end_time=end)
                    else:
                        puzzle_db.insert('qa_crashcount', app_name=apps[i]['app_name'],
                                         app_platform=apps[i]['app_platform'],
                                         crash_count=0, start_time=start, end_time=end, updated_at=end)
                else:

                    if not is_old:
                        now = datetime.datetime.now()
                        now = now.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        now = end
                    puzzle_db.update('qa_crashcount', where="id=" + str(crash_count[0]['id']),
                                     crash_count=0,
                                     start_time=start, end_time=end, updated_at=now)
            if context != '':
                send_mail(sub, context, 'Crash No-Reply', mail_to)
            data['result'] = context
            if not is_old:
                apps_tmp = puzzle_db.query("SELECT * FROM qa_crashcount_limit ORDER BY id")
                for item in apps_tmp:
                    file_name = str(item['id'])
                    path = 'static/chart/'
                    file_object = open(path + file_name + '.js', 'w')
                    js = get_chart_js(item['app_name'], item['app_platform'])
                    file_object.write(js)
                    file_object.close()
                    os.system(common.phantomjs_path + ' static/js/highcharts-convert.js '
                                                  '-infile ' + path + file_name + '.js -outfile ' + path + file_name + '.png')
            puzzle_db.insert('qa_jobtime',start=start,end=end)
        except Exception as err:
            error = '错误信息：' + error + str(err)
            data['result'] = error
            print error
            send_mail('[' + start + ']crash信息更新失败', error, 'Crash No-Reply')
        if error == '':
            result += start+'至'+end+ '更新成功<br>'
        else:
            result += start+'至'+end+ '更新失败 '+error+'<br>'

        start_tmp = start_tmp + datetime.timedelta(seconds=600)
        end_tmp = end_tmp + datetime.timedelta(seconds=600)

        print result
    if lack_context !='':
        send_mail('补Crash数据',lack_context,'Crash No-Reply')
    return result


def get_chart_js(app_name, app_platform, start=None, end=None):
    now = datetime.datetime.now()
    dt_date = now.strftime('%Y-%m-%d')
    if not start or not end:
        dt_date = datetime.datetime.now()
        dt_date = dt_date.strftime('%Y-%m-%d')
        start = dt_date
        end = dt_date
        start = start + ' 00:00:00'
        end = end + ' 23:59:59'
    from controllers.Monitor import get_all_data

    result = get_all_data(app_name, app_platform, start, end)
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

        js += "[" + utc + "," + str(i[1]) + "],"
    js += "]\
                },\
                {\
                    name: 'lastweek',\
                    data:["
    for i in result[1]:
        utc = get_utc(i[0], 7)
        js += "[" + utc + "," + str(i[1]) + "],"
    js += "]\
                }\
            ]\
        };\
        Highcharts.setOptions({\
            global: {\
                useUTC: false\
            }\
        });"
    return js


def get_utc(timestamp, days=0):
    utc = str((timestamp + days * 24 * 60 * 60) * 1000)


