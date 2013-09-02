#encoding=utf8
import web
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from config import settings
import time
import datetime
from model.GlobalFunc import send_mail

render = settings.render
data = {'pageIndex':'crash'}
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
            crash_count=''

        if app_name and app_platform and crash_count:
            crash_count = int(crash_count)
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            value = {'app_name':app_name,'app_platform':app_platform}
            crash_limit = puzzle_db.select('qa_crashcount_limit',where='app_name=$app_name AND app_platform=$app_platform',
                                           vars=value)
            if len(crash_limit) == 0:
                puzzle_db.insert('qa_crashcount_limit',app_name=app_name,app_platform=app_platform,
                             crash_count=crash_count,updated_at=now)
            else:
                puzzle_db.update('qa_crashcount_limit',where="id="+str(crash_limit[0]['id']),
                                 crash_count=crash_count,updated_at=now)

        data['crash_limit']=puzzle_db.select('qa_crashcount_limit',order="app_name,app_platform")
        data['apps'] = puzzle_db.query('SELECT DISTINCT app_name FROM qa_crashcount_limit')
        data['params'] = {'app_name':app_name,'app_platform':app_platform,'crash_count':crash_count}
        return render.crashSet(data=data)


class Job:
    def GET(self):
        # try:
            data['result'] = ''
            start =''
            params = web.input()
            start = params.get('start')
            end = params.get('end')
            #synctime = ama_db.select('bs_synctime',where ='Item = "crashdatasync"')
            # if len(synctime) ==0:
            #     now = datetime.datetime.now()
            #     format_now = str(now.strftime('%Y-%m-%d %H:%M:%S'))
            #     send_mail('['+format_now+']缺少同步时间','缺少同步时间')
            #     return render.CrashJob(data=data)
            # else:
            #     end = str(synctime[0]['datetime'])
            # end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
            # start = str(end - datetime.timedelta(minutes=20))
            apps_tmp = puzzle_db.query("SELECT * FROM qa_crashcount_limit")
            apps = {}
            for app in apps_tmp:
                id = len(apps)
                apps[id] ={}
                for key in app:
                    apps[id][key] =app[key]

            if not start or not end:
                now = datetime.datetime.now()
                format_now = str(now.strftime('%Y-%m-%d %H:%M:%S'))
                send_mail('['+format_now+']缺少同步时间','缺少同步时间')
                return render.CrashJob(data=data)


            crash = ama_db.query("SELECT c.AppName AS app_name ,c.AppPlatform AS app_platform, "
                                 "count(*) AS count "
                                 "FROM crashdata c "
                                 "LEFT JOIN bs_appid b "
                                 "ON c.AppName = b.AppName AND c.AppPlatform=b.AppPlatform AND c.AppVer = b.AppVer "
                                 "WHERE c.ExecDateTime < $end AND	c.ExecDateTime >= $start AND b.isShow = 1 "
                                 "GROUP BY c.AppName,c.AppPlatform",vars = {'start':start,'end':end})
            sub = '['+start+']crash report'
            context = ''
            for item in crash:
                for i in apps:
                    app =apps[i]
                    res = False
                    if item['app_name'] == app['app_name'] and item['app_platform'] == app['app_platform']:
                        del apps[i]
                        break


                value = {'app_name':item['app_name'],'app_platform':item['app_platform'],
                        'start_time':start,'end_time':end}
                crash_count = puzzle_db.select('qa_crashcount',where = "app_name=$app_name AND app_platform =$app_platform "
                                                         " AND start_time =$start_time AND end_time=$end_time",vars=value)
                if len(crash_count) == 0:
                    puzzle_db.insert('qa_crashcount',app_name = item['app_name'],app_platform = item['app_platform'],
                                 crash_count=item['count'],start_time=start,end_time=end)
                else:
                    now = datetime.datetime.now()
                    now = now.strftime('%Y-%m-%d %H:%M:%S')
                    puzzle_db.update('qa_crashcount',where="id="+str(crash_count[0]['id']),crash_count=item['count'],
                                     start_time = start,end_time = end,updated_at =now)

                crash_limit=puzzle_db.select('qa_crashcount_limit',where = "app_name=$app_name "
                                                                           "AND app_platform =$app_platform ",vars=value)

                if len(crash_limit) == 1:
                    limit_count = crash_limit[0]['crash_count']
                    if item['count'] > limit_count:

                        context += item['app_name']+item['app_platform']+'crash 实际量为'\
                                  +str(item['count'])+',超过设定值'+str(limit_count)+'<br>'

                else:
                    context += item['app_name']+item['app_platform']+'未设置crash数量<br>'
            for i in apps:
                puzzle_db.insert('qa_crashcount',app_name = apps[i]['app_name'],app_platform = apps[i]['app_platform'],
                                 crash_count=0,start_time=start,end_time=end)
            if context!='':
                send_mail(sub,context)
            data['result'] = context
        # except Exception as err:
        #     error = '错误信息：'+str(err)
        #     data['result'] = '错误信息：'+error
        #     send_mail('['+start+']crash信息更新失败',error)
            return render.crashJob(data=data)