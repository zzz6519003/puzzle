#!/usr/bin/python
#encoding=utf8
import json
import sys
import web
reload(sys)
sys.setdefaultencoding('utf8')
import os
import datetime
sys.path.append("../model")
from GlobalFunc import send_mail
sys.path.append("../config")
import common
import dbSettings
import time
data={}
time_interval = 600

def doWork(gearmanWorker, job):
    result = ''
    lack_context = ''
    puzzle_db = dbSettings.getConnectionV2('puzzle')
    ama_db = dbSettings.getConnectionV2('ama')
    params = json.loads(job.data)
    job_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #mail_to = ["yuetingqian@anjuke.com","vingowang@anjukeinc.com","clairyin@anjuke.com","angelazhang@anjuke.com"]
    mail_to = ["yuetingqian@anjuke.com", "vingowang@anjukeinc.com"]
    param_start = params['start']
    param_end = params['end']
    try:
        db_end_obj = puzzle_db.query("SELECT end FROM qa_jobtime WHERE end <=$end and type=2 ORDER BY end DESC LIMIT 1",
                vars={'end':param_end})
        end_time = time_rounding(param_end, time_interval)

        if len(db_end_obj) == 0:
            db_end_time = end_time - datetime.timedelta(seconds=time_interval)
        else:
            db_end_time = time_rounding(str(db_end_obj[0]['end']), time_interval)

        if end_time <= db_end_time:
            result += '已存在数据，不需要更新'
            return result

        diff_time = int((end_time - db_end_time).total_seconds())
        count = diff_time/time_interval
        mail_body = ''
        for i in range(0, count):
            diff_start = i * time_interval + 1
            diff_end = (i + 1) * time_interval
            start = str(db_end_time + datetime.timedelta(seconds=diff_start))
            end = str(db_end_time + datetime.timedelta(seconds=diff_end))
            if i != count -1:
                lack_context += '%s-%s缺少数据<br>' % (start, end)

            apps = puzzle_db.query("SELECT l.app_name AS app_name, l.app_platform AS app_platform, \
                                    t.crash_title AS crash_title, t.crash_count AS crash_count \
                                    FROM qa_crashtitle AS t, qa_crashcount_limit AS l \
                                    WHERE t.app_id = l.id")
            for app in apps:
                value = {
                        'app_name': app['app_name'],
                        'app_platform': app['app_platform'],
                        'crash_title': '%'+ app['crash_title'] + '%',
                        'start': start,
                        'end': end
                        }

                crashes = ama_db.query("SELECT DISTINCT c.AppName app_name, c.AppPlatform app_platform, c.APPVer app_ver, \
                        c.CrashTitle crash_title, c.CrashDetail, FROM_UNIXTIME(c.CrashTime) crash_time , \
                        c.DeviceID, c.NewID, c.AppPM, c.Model, c.OSVer \
                        FROM crashdata c \
                        LEFT JOIN bs_appid b \
                        ON c.AppName = b.AppName AND c.AppPlatform = b.AppPlatform AND c.AppVer = b.AppVer \
                        WHERE c.AppName = $app_name AND c.AppPlatform = $app_platform \
                        AND c.edt >= $start AND c.edt <= $end \
                        AND c.CrashTitle LIKE $crash_title AND b.isShow = 1",vars=value)

                crash_count = len(crashes)
                if crash_count >= app['crash_count']:
                    mail_body += '【%s-%s】%s%s重要crash(title:%s)共有%d个，达到或超过设置值%d个，具体如下:<br>' \
                            % (start, end, app['app_name'], app['app_platform'], app['crash_title'], crash_count, app['crash_count'])
                    style = 'style="font-size:13px;font-family:Arial;background:#F7F7F0;border:1px solid #D7D7D7;' \
                            'border-collapse: collapse;font-weight:bold;padding:2px 8px;vertical-align:bottom;' \
                            'white-space:nowrap;border-image:initial;text-align:left;"'
                    mail_body += '<table style="TABLE-LAYOUT: fixed;; WORD-BREAK: break-all;;border-collapse: collapse">'
                    mail_body += '<tr><td ' + style + '>id</td><td ' + style + '>app</td><td ' + style + '>os</td>' \
                                 '<td ' + style + '>version</td><td  ' + style + ' width="10%">title</td><td ' + style + '>DeviceID' \
                                 + '</td><td ' + style + '>NewID</td><td '+ style + '>time</td></tr>'
                    i = 1
                    for detail in crashes:
                        mail_body += '<tr><td ' + style + '>' + str(i) + '</td><td ' + style + '>' + detail['app_name'] + \
                                   '</td><td ' + style + '>' + detail['app_platform'] + '</td ' + style + '><td ' + style + '>' \
                                   + detail['app_ver'] + '</td><td ' + style + ' nowrap>' + detail['crash_title'] \
                                   + '</td><td ' + style + '>' + detail['DeviceID'] + '</td><td ' + style + '>' + detail['NewID'] \
                                   + '</td><td ' + style + '>' + str(detail['crash_time']) + '</td></tr>'
                        i = i + 1

                    mail_body += '</table><br>'
        if mail_body != '':
            send_mail('Important Crash', mail_body, 'Crash No-Replay', mail_to)
        if lack_context !='':
            send_mail('补crash_title数据', lack_context, 'Crash No-Replay')
        puzzle_db.insert('qa_jobtime', start=start, end=end, type=2, updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        result += mail_body
    except Exception as e:
        send_mail('crash_title检查失败', e,'Crash No-Replay')
    dbSettings.close_db(puzzle_db)
    dbSettings.close_db(ama_db)
    return result.encode('utf-8')


def time_rounding(time_str, time_interval, time_formate='%Y-%m-%d %H:%M:%S'):
    '''
    时间取整，如time_interval=600,即将time_str变成小于该时间中最大10分钟的倍数时间
    如2013-10-10 3:01:11 变成datetime类型的2013-10-10 3:00:00
    '''
    ptime = datetime.datetime.strptime(time_str, time_formate)
    timestamp = time.mktime(ptime.timetuple())
    count = int(timestamp/time_interval)
    rounding = int(count*600)
    result = datetime.datetime.fromtimestamp(rounding)
    return result

