#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from config import settings
import json
import web
import string
import time
import urllib

render = settings.render
data = {'pageIndex':'report'}
puzzle_db = settings.puzzle_db
pmt_db = settings.pmt_db
ibug_db = settings.ibug_db


class Index:
    def GET(self):
        data = {'pageIndex':'report'}
        data = get_select(data)
        params = web.input()
        appName = params.get('appName')
        category = params.get('category')
        version = params.get('version')
        if appName:
            appName = urllib.unquote(appName)
        data['params'] = {'appName':appName,'category':category,'version':version}

        project_list = get_project_list(appName,category,version)
        data['project_bug'] = {}
        index = 0
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug'][index] = {}

            devs = get_owners(pmt_id,'dev')
            dev_str = get_owner_str(devs)
            qas = get_owners(pmt_id,'qa')
            qa_str = get_owner_str(qas)
            counts = puzzle_db.select('rp_projectbug',where ='pmtId = $pmt_id',vars = {'pmt_id':pmt_id})
            if len(counts):
                count = counts[0]
            else :
                count =  {}.fromkeys(('app', 'api','product','p1','p2','p3','p4','p5','test','dev','prerelease','production'),0)

            total = count['app']+ count['api']+count['product']
            data['project_bug'][index] = filter_project_info(count,project,dev_str,qa_str)
            rp_projectList = puzzle_db.select('rp_projectList',where='pmtId=$pmt_id',vars = {'pmt_id':pmt_id})
            if len(rp_projectList) == 1:
                rate = rp_projectList[0]['rate']
            else:
                rate = ''
            data['project_bug'][index]['rate'] = rate
            data['project_bug'][index]['total'] = total
            data['project_bug'][index]['created'] = get_created_time(pmt_id)
            index +=1

        return render.reportIndex(data=data)

class Reason:
    def GET(self):
        data = {'pageIndex':'report'}
        data = get_select(data)
        params = web.input()
        appName = params.get('appName')
        category = params.get('category')
        version = params.get('version')
        if appName:
            appName = urllib.unquote(appName)
        data['params'] = {'appName':appName,'category':category,'version':version}

        reason_all_tmp = ibug_db.select('dd_common',where = "type='reason'",order = 'sort')
        data['th']={}
        for reason in reason_all_tmp:
            id = reason['id']
            data['th'][id] = {'name':reason['name'],'count':0}
        data['th'][0] ={'name':'无原因','count':0}

        project_list = get_project_list(appName,category,version)
        data['project_bug_reason'] = {}
        index = 0
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug_reason'][index] = {}
            data['project_bug_reason'][index]['project'] ={}
            data['project_bug_reason'][index]['reason'] ={}
            data['project_bug_reason'][index]['total'] = 0
            data['project_bug_reason'][index]['project'] ={'name':get_pro_name(project['appName'],project['category'],project['version']),'pmt_id':pmt_id}
            devs = get_owners(pmt_id,'dev')
            qas = get_owners(pmt_id,'qa')
            data['project_bug_reason'][index]['project']['developer'] = get_owner_str(devs)
            data['project_bug_reason'][index]['project']['qa'] = get_owner_str(qas)
            data['project_bug_reason'][index]['project']['endtime'] = format_time(project['endDate'])

            data['project_bug_reason'][index]['project']['created'] = get_created_time(pmt_id)

            project_bug_reason = puzzle_db.select('rp_projectbug_type',where="pmtId = $pmt_id AND type ='reason'",vars = {'pmt_id':pmt_id})
            bug_reason = {}
            for item in project_bug_reason:
                bug_reason[item['com_id']] = {'count':item['count']}
                data['project_bug_reason'][index]['total'] += bug_reason[item['com_id']]['count']

            for id in data['th']:
                if  id in bug_reason :
                    data['project_bug_reason'][index]['reason'][id] = bug_reason[id]
                    data['th'][id]['count'] +=1;
                else:
                    data['project_bug_reason'][index]['reason'][id] = {'count':0}
            index+=1

        for id in data['th'].keys() :
            if data['th'][id]['count'] ==0:
                data['th'].pop(id)
                for index in data['project_bug_reason']:
                    data['project_bug_reason'][index]['reason'].pop(id)
            else :
                for index in data['project_bug_reason']:
                    data['project_bug_reason'][index]['reason'][id]['name'] = data['th'][id]['name']
        data['colspan'] = len(data['th'])+1
        return render.reportReason(data=data)

class Component:
    def GET(self):
        data = {'pageIndex':'report'}
        data = get_select(data)

        params = web.input()
        appName = params.get('appName')
        if appName :
            appName = urllib.unquote(appName)

        category = params.get('category')
        version =params.get('version')
        data['params'] = {'appName':appName,'category':category,'version':version}

        component_all_tmp = ibug_db.select('dd_component')
        data['th'] = {}
        for com in component_all_tmp:
            id = com['int']
            data['th'][id] = {'name':com['name'],'count':0}

        project_list = get_project_list(appName,category,version)
        data['project_bug_component'] = {}
        index = 0
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug_component'][index] = {}
            data['project_bug_component'][index]['project'] = {'name':get_pro_name(project['appName'],project['category'],project['version']),'pmt_id':pmt_id}
            devs = get_owners(pmt_id,'dev')
            qas = get_owners(pmt_id,'qa')
            data['project_bug_component'][index]['project']['developer'] = get_owner_str(devs)
            data['project_bug_component'][index]['project']['qa'] = get_owner_str(qas)
            data['project_bug_component'][index]['project']['endtime'] = format_time(project['endDate'])
            data['project_bug_component'][index]['component'] ={}
            data['project_bug_component'][index]['total'] = 0

            data['project_bug_component'][index]['project']['created'] = get_created_time(pmt_id)

            project_bug_component = puzzle_db.select('rp_projectbug_type',where ="pmtId =$pmt_id AND type='component'",vars = {'pmt_id':pmt_id})
            bug_component = {}
            for item in project_bug_component:
                bug_component[item['com_id']] = {'count':item['count']}
                data['project_bug_component'][index]['total'] += bug_component[item['com_id']]['count']

            for id in data['th']:
                if id in bug_component :
                    data['project_bug_component'][index]['component'][id] = bug_component[id]
                    data['th'][id]['count'] +=1
                else:
                    data['project_bug_component'][index]['component'][id] = {'count':0}
            index+=1
        for id in data['th'].keys() :
            if data['th'][id]['count'] == 0:
                data['th'].pop(id)
                for index in data['project_bug_component']:
                    data['project_bug_component'][index]['component'].pop(id)
            else:
                for index in data['project_bug_component']:
                    data['project_bug_component'][index]['component'][id]['name'] = data['th'][id]['name']

        data['colspan'] = len(data['th'])+1

        return render.reportComponent(data=data)

class Developer:
    def GET(self):
        data = {'pageIndex':'report'}
        data = get_select(data)

        params = web.input()
        appName = params.get('appName')
        if appName :
            appName = urllib.unquote(appName)

        category = params.get('category')
        version =params.get('version')
        project_time = params.get('project_time')
        if not project_time:
            project_time = ''
        data['params'] = {'appName':appName,'category':category,'version':version,'project_time':project_time}

        data['data'] = {}
        project_list = get_project_list(appName,category,version,project_time)

        index = 0
        for project in project_list:
            pmt_id = project['pmtId']
            users = {}
            devs = get_owners(pmt_id,'dev')
            dev_str = get_owner_str(devs)
            qas = get_owners(pmt_id,'qa')
            qa_str = get_owner_str(qas)

            project_info ={}
            project_info['pmt_id'] = pmt_id
            project_info['name'] = get_pro_name(project['appName'],project['category'],project['version'])
            project_info['endtime'] = format_time(project['endDate'])
            project_info['developer'] = dev_str
            project_info['qa'] = qa_str
            data['data'][index] ={'project':project_info}


            project_info['created'] = get_created_time(pmt_id)

            devs_bug = puzzle_db.select('rp_developer',where="pmtId = $pmt_id",vars={'pmt_id':pmt_id},order='user_from ASC')
            max_id = 0
            result = {}.fromkeys(('chinese_name','total','workload','workload_div','unclose','close_div','reject','reopen','lose_repair_div','repair_time','major_bug','repair_time_div','daily_to_rc','daily_to_rc_div'),'')
            for item in devs_bug:
                user_id = len(users)
                total = item['total']
                user = item
                if item['user_from'] ==1:
                    workload = item['workload']
                else:
                    user['workload'] = 'N/A'
                    workload = 'N/A'
                user['total'] = total
                user['workload_div'] = div(total,workload)
                user['close_div'] = div(total-user['unclose'],total)
                user['lose_repair_div'] = div(user['reject']+user['reopen'],total)
                user['repair_time_div'] = div(user['repair_time'],user['major_bug'])
                user['daily_to_rc_div'] = div(user['daily_to_rc'],user['rc'])
                users[user_id] = user
                max_id = user_id+1

            if max_id > 0 :
                total_id = max_id
                user_tmp = {}.fromkeys(('total','workload','unclose','reject','reopen','repair_time','major_bug','daily_to_rc','rc'),0)
                for user_id in users:
                    for key in users[user_id]:
                        if key in user_tmp and users[user_id][key]!='N/A':
                            user_tmp[key] += users[user_id][key]
                user_tmp['chinese_name'] = 'total'
                total = user_tmp['total']
                user_tmp['workload_div'] = div(total,user_tmp['workload'])
                user_tmp['close_div'] = div(total-user_tmp['unclose'],total)
                user_tmp['lose_repair_div'] = div(user_tmp['reject']+user_tmp['reopen'],total)
                user_tmp['repair_time_div'] = div(user_tmp['repair_time'],user_tmp['major_bug'])
                user_tmp['daily_to_rc_div'] = div(user_tmp['daily_to_rc'],user_tmp['rc'])
                users[total_id] = user_tmp
                for user_id in users:
                    if user_id != total_id:
                        for key in users[user_id]:
                            if key in result:
                                if users[user_id]['user_from'] ==2  and key =='chinese_name':
                                    color ='#B0B85E'
                                else:
                                    color = ''
                                result[key] += '<span  style="background-color:'+color+';">'+str(users[user_id][key]) + '<br></span>'
                for key in users[total_id]:
                    if key in result:
                        result[key] += '<span>' + str(users[total_id][key]) + '<br></span>'

            data['data'][index]['count'] = result
            data['data'][index]['count_s'] = users
            index+=1
        return render.reportDeveloper(data=data)

class Qa:
    def GET(self):

        data = {'pageIndex':'report'}
        data = get_select(data)

        params = web.input()
        appName = params.get('appName')
        if appName :
            appName = urllib.unquote(appName)

        category = params.get('category')
        version =params.get('version')
        project_time = params.get('project_time')
        if not project_time:
            project_time = ''

        data['params'] = {'appName':appName,'category':category,'version':version,'project_time':project_time}

        project_list = get_project_list(appName,category,version,project_time)

        data['data'] = {}
        index = 0
        for project in project_list:
            pmt_id = project['pmtId']

            users = {}

            devs = get_owners(pmt_id,'dev')
            dev_str = get_owner_str(devs)
            qas = get_owners(pmt_id,'qa')
            qa_str = get_owner_str(qas)

            project_info = {}
            project_info['pmt_id'] = pmt_id
            project_info['name'] = get_pro_name(project['appName'],project['category'],project['version'])
            project_info['endtime'] = format_time(project['endDate'])
            project_info['developer'] = dev_str
            project_info['qa'] = qa_str
            project_info['created'] = get_created_time(pmt_id)

            data['data'][index] ={'project':project_info}

            qas_bug = puzzle_db.select('rp_qa',where = "pmtId = $pmt_id",vars = {'pmt_id':pmt_id},order='user_from')
            max_id = 0
            result = {}.fromkeys(('total','workload','workload_div','p1','p2','p3','p4','dailybuild','no_dailybuild','dr_div','chinese_name'),'')

            for item in qas_bug:
                user_id = len(users)
                user = item
                total = item['total']
                if item['user_from'] ==1:
                    workload = item['workload']
                else:
                    user['workload'] = 'N/A'
                    workload = 'N/A'
                user['total'] = total
                user['workload_div'] = div(total,workload)
                dailybuild = user['dailybuild']
                no_dailybuild = total - dailybuild
                user['no_dailybuild'] = no_dailybuild
                user['dr_div'] = div(dailybuild,no_dailybuild)
                users[user_id] = user
                max_id = user_id+1

            if max_id > 0:
                total_id = max_id
                user_tmp = {}.fromkeys(('total','workload','p1','p2','p3','p4','dailybuild','no_dailybuild'),0)
                for user_id in users :
                    for key in users[user_id] :
                        if key in user_tmp and users[user_id][key]!='N/A':
                            user_tmp[key] +=  users[user_id][key]
                users[total_id] = user_tmp
                users[total_id]['chinese_name'] = 'total'
                users[total_id]['workload_div'] = div(users[total_id]['total'],users[total_id]['workload'])
                users[total_id]['dr_div'] = div(users[total_id]['dailybuild'],users[total_id]['no_dailybuild'])
                for user_id in users:
                    if user_id != total_id:
                        for key in users[user_id]:
                            if key in result and key not in{'p1','p2','p3','p4'}:
                                if key in result:
                                    if users[user_id]['user_from'] ==2  and key =='chinese_name':
                                        color ='#B0B85E'
                                    else:
                                        color = ''
                                    result[key] += '<span  style="background-color:'+color+';">'+str(users[user_id][key])+'<br></span>'

                for key in users[total_id]:
                    if key in result:
                        result[key] += '<span>'+str(users[total_id][key])+'<br><span>'
            data['data'][index]['count'] = result
            data['data'][index]['count_s'] =users
            index+=1

        return render.reportQa(data=data)

class Detail:
    def GET(self):
        params = web.input()
        pmt_id = params.get('pmt_id')
        cn_name = params.get('cn_name')
        page = params.get('page')
        location = params.get('location')
        tickets = {}
        if page == 'qa':
            if location == 'total':
                tickets = get_qa_bugs_from_puzzle(pmt_id,cn_name)
            elif location in ('p1','p2','p3','p4'):
                tickets = get_qa_priority_bugs_from_puzzle(pmt_id,location)
            elif location == 'dailybuild':
                tickets = get_qa_dailybuild_bugs_from_puzzle(pmt_id,cn_name,True)
            elif location == 'no_dailybuild':
                tickets = get_qa_dailybuild_bugs_from_puzzle(pmt_id,cn_name,False)
        elif page =='developer':
            if location == 'total':
                tickets = get_dev_bugs_from_puzzle(pmt_id,cn_name)
            elif location =='unclose':
                tickets = get_dev_unclose_bugs_from_puzzle(pmt_id,cn_name)
            elif location =='reopen':
                tickets = get_dev_reopen_bugs_from_puzzle(pmt_id,cn_name)
            elif location =='reject':
                tickets = get_dev_reject_bugs_from_puzzle(pmt_id,cn_name)
            elif location =='daily_to_rc':
                tickets = get_dev_daily_to_rc_bugs_from_puzzle(pmt_id,cn_name)
        elif page =='index':
            if location =='total':
                tickets = puzzle_db.select('ticket',where="pmtId = $pmt_id AND environment<>'test'",
                        vars={'pmt_id':pmt_id})
            elif location == 'app':
                tickets = puzzle_db.query("SELECT * FROM ticket \
                        WHERE pmtId=$pmt_id AND component NOT LIKE '%api%' \
                        AND reason NOT LIKE '%产品设计%' AND environment !='test'",vars={'pmt_id':pmt_id})
            elif location == 'api':
                tickets = puzzle_db.query("SELECT * FROM ticket \
                        WHERE pmtId=$pmt_id AND component LIKE '%api%' \
                        AND reason NOT LIKE '%产品设计%' AND environment !='test'",vars={'pmt_id':pmt_id})
            elif location == 'product':
                tickets = puzzle_db.query("SELECT * FROM ticket \
                        WHERE pmtId=$pmt_id AND reason LIKE '%产品设计%' \
                        AND environment !='test'",vars={'pmt_id':pmt_id})
            elif location in ('p1','p2','p3','p4','p5'):
                tickets = puzzle_db.query("SELECT * FROM ticket \
                        WHERE pmtId=$pmt_id AND component NOT LIKE '%api%' \
                        AND priority  LIKE $priority AND environment !='test' AND reason  NOT LIKE '%产品设计%' ",vars={'pmt_id':pmt_id,'priority':location+'%'})
            elif location in ('test','dev','prerelease','production'):
                tickets = puzzle_db.query("SELECT * FROM ticket \
                        WHERE pmtId=$pmt_id AND component NOT LIKE '%api%' \
                        AND environment=$environment AND reason  NOT LIKE '%产品设计%' ",vars={'pmt_id':pmt_id,'environment':location})
        elif page == 'reason':
            sql = "SELECT * FROM ticket WHERE pmtId=$pmt_id AND component NOT LIKE '%api%' AND reason  NOT LIKE '%产品设计%' "
            if location =='无原因':
                sql += "AND reason = ''"
            elif location !='total':
                sql += "AND reason = $reason"
            tickets = puzzle_db.query(sql,vars={'pmt_id':urllib.unquote(pmt_id),'reason':location})
        elif page =='component':
            sql = "SELECT * FROM ticket WHERE pmtId=$pmt_id AND reason NOT LIKE '%产品设计%' "
            if location !='total':
                sql += "AND component =$component"
            tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'component':urllib.unquote(location)})

        data['tickets'] = tickets
        return render.reportDetail(data=data)



class Update:
    def GET(self):
        params = web.input()
        rate = params.get('rate')
        is_updated = params.get('is_updated')
        update= params.get('update')
        if rate:
            data['rate'] = rate
        else:
            data['rate'] = ''
        if is_updated:
            data['is_updated'] = is_updated
        else:
            data['is_updated'] = ''
        if update:
            data['update'] = update
        else:
            data['update'] = ''
            update = 0
        data['pmt_id_job'] =''
        data['pmt_id_pro'] =''
        data['info'] = ''
        #获取当前日期
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))
        if int(update)==1:
            pmt_id = params.get('pmt_id_job')

            if pmt_id :
                data['pmt_id_job'] = pmt_id
            else:
                data['pmt_id_job'] = ''
            value = {'pmt_id':pmt_id}
            from PuzzleBackGround import PuzzleBackGroundCommands
            data['info'] = PuzzleBackGroundCommands.doWork_calculateBugCount(value)
        if int(update)==2:
            pmt_id = params.get('pmt_id_pro')

            if pmt_id :
                data['pmt_id_pro'] = pmt_id
            else:
                data['pmt_id_pro'] = ''
            try:
                rp_projectList = puzzle_db.select('rp_projectList',where='pmtId=$pmt_id',vars={'pmt_id':pmt_id})
                if len(rp_projectList) == 1:
                    puzzle_db.update('rp_projectList',where ='pmtId=$pmt_id',vars={'pmt_id':pmt_id},rate=rate,is_updated=is_updated,last_updated=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                else:
                    puzzle_db.insert('rp_projectList',pmtId=pmt_id,rate=rate,is_updated=is_updated)
                data['info'] = '项目信息更新成功'
            except:
                data['info'] = '项目信息更新失败'


            #获取数据
        return render.reportUpdate(data=data)

class Job:
    def GET(self):
        import urllib2
        import urllib
        data = {'pageIndex':'report','error':''}
        projects = puzzle_db.select('rp_projectList',where="is_updated=1")
        for project in projects:
            #url = "http://puzzle.corp.anjuke.com/report/update?pmt_id_job="+str(project['pmtId'])+"&update=1"
            url = "http://puzzle.corp.anjuke.com/report/update?pmt_id_job="+str(project['pmtId'])+"&update=1"
            fd = urllib2.urlopen(url)
            content = fd.read()

            if content.find('统计信息更新失败')>0:
                data['error'] += str(project['pmtId'])+'更新失败.<br>'
            else:
                data['error'] += str(project['pmtId'])+'更新成功.<br>'

        return render.reportJob(data=data)


def get_qa_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId=$pmt_id "
    if cn_name != 'total':
        sql += " AND reporter=$cn_name"
    tickets = puzzle_db.query(sql,vars = {'pmt_id':pmt_id,'cn_name':cn_name})
    if cn_name == 'total':
        ticket = puzzle_db.select('ticket',where="pmtId=$pmt_id",vars={'pmt_id':pmt_id})
    else:
        ticket = puzzle_db.select('ticket', where=" pmtId=$pmt_id AND reporter = $cn_name",vars ={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets

def get_qa_priority_bugs_from_puzzle(pmt_id,location):
    tickets = puzzle_db.query("SELECT * FROM ticket WHERE pmtId = $pmt_id AND environment='PreRelease' AND priority LIKE $priority",vars={'pmt_id':pmt_id,'priority':location+'%'})
    return tickets

def get_qa_dailybuild_bugs_from_puzzle(pmt_id,cn_name,is_daily):
    vars= {'pmt_id':pmt_id,'cn_name':cn_name}
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id AND environment "
    if is_daily ==True:
        sql += "='test' "
    else:
        sql += "!='test'"
    if cn_name !='total':
        sql += "AND reporter = $cn_name"
    tickets = puzzle_db.query(sql,vars)
    return tickets

def get_dev_bugs_from_puzzle(pmt_id,cn_name):
    if cn_name =='total':
        tickets = puzzle_db.select('ticket', where="pmtId=$pmt_id AND environment !='test' AND component NOT LIKE '%api%' AND reason !='产品设计'",vars ={'pmt_id':pmt_id})
    else:
        tickets = puzzle_db.select('ticket', where=" pmtId=$pmt_id AND owner = $cn_name AND environment !='test' AND reason !='产品设计' ",vars ={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets

def get_dev_unclose_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id AND status !='closed' AND environment!='test' "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets

def get_dev_reject_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id AND is_reject=1 AND environment!='test' AND reason !='产品设计' "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets


def get_dev_reopen_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id AND is_reopen=1 AND environment!='test' AND reason !='产品设计' "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets

def get_dev_daily_to_rc_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id  AND is_daily_to_rc=1 AND reason !='产品设计' "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets



def filter_project_info(fl_project,project,dev_str,qa_str):

    fl_project['pmt_id'] = project['pmtId']
    fl_project['name'] = get_pro_name(project['appName'],project['category'],project['version'])
    fl_project['endtime'] = format_time(project['endDate'])
    fl_project['developer'] = dev_str
    fl_project['qa'] = qa_str

    return fl_project

def get_os_img(category):
    if int(category) ==1:
        img ='i.png'
    else:
        img = 'a.png'
    return '<img border="0" src="/static/img/'+img+'" width="20" height="20"> '

def get_pro_name(appName,category,version):
    return get_os_img(category)+appName+' '+version+' '


def get_created_time(pmt_id):
    created = '暂无更新时间'
    rp_projectList = puzzle_db.select('rp_projectList',where='pmtId=$pmt_id',vars={'pmt_id':pmt_id})
    if len(rp_projectList) ==1:
        tmp = rp_projectList[0]
        created =  format_time(datetime_to_timestamp(tmp['last_updated']),'%Y-%m-%d %H:%M')
    return created



def get_owners(pmt_id,type):
    if type =='dev':
        table = 'rp_developer'
    else :
        table = 'rp_qa'
    owners = puzzle_db.select(table,where ='pmtId = $pmt_id',vars ={'pmt_id':pmt_id},order ='id')
    return owners


def get_owner_str(owners):
    str = ''

    for owner in owners:
        if int(owner['user_from']) == 2:
            bgcolor = '#B0B85E'
        else:
            bgcolor = ''
        str += '<span style="background-color:'+bgcolor+';">'+ owner['chinese_name'] +'<br></span>'
    return str

def get_project_list(appName,category,version,project_time=None):
    if not appName and not category and not version and not project_time:
        return {}

    sql = "SELECT b.pmtId AS pmtId,b.version AS version,\
    b.appName AS appName,b.category AS category,e.startDate AS endDate \
    FROM (SELECT p.id AS id,p.pmtId AS pmtId,\
    p.version AS version,a.appGroup as appName,a.category AS category \
    FROM projectlist AS p ,applist AS a \
    WHERE p.appId = a.id "
    value ={}

    if appName :
        sql += "AND a.appGroup = $appName "
        value['appName'] = appName
    if category :
        sql += "AND a.category=$category "
        value['category'] = category
    if version :
        sql += "AND p.version = $version "
        value['version'] = version
    sql += ") as b \
    LEFT JOIN projectevent AS e \
    ON b.id = e.projectId AND e.category =10  \
    LEFT JOIN rp_projectList AS rp \
    ON b.pmtId = rp.pmtId "
    if project_time:
        sql += "WHERE rp.project_time = $project_time "
        value['project_time'] = project_time
    sql +="GROUP BY  appName,category,version,pmtId ORDER BY pmtId DESC "
    project_list = puzzle_db.query(sql,vars = value)
    return project_list

def get_select(data):
    data['appName'] = {}
    index = 0
    dict_index = {}
    data['version'] = {}
    appNames = puzzle_db.query("SELECT DISTINCT appGroup AS appName FROM appList WHERE appGroup <>'' ORDER BY id")
    for item in appNames:
        data['appName'][index] = item['appName']
        dict_index[item['appName']] = index
        data['version'][index] = {}
        index +=1

    versions = puzzle_db.query("SELECT DISTINCT a.appGroup as appName ,p.version as version \
                                FROM applist AS a,projectlist AS p \
                                WHERE a.id = p.appId AND appGroup <> '' ORDER BY version DESC")
    for item in versions:
        index = dict_index[item['appName']]
        pos = len(data['version'][index])
        data['version'][index][pos] = item['version']
    return data

def div(dividend,divisor):
    if divisor=='N/A' or divisor ==0 :
        return '-'
    else :
        return round(float(dividend)/float(divisor),2)

def format_time(timestamp,format_t=None):
    import time
    if not format_t:
        format_t = '%Y-%m-%d'
    if timestamp :
        format_time = time.strftime(format_t,time.localtime(timestamp))
    else :
        format_time = ''
    return format_time

def datetime_to_timestamp(dt):
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    #将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(str(dt), '%Y-%m-%d %H:%M:%S'))
    return int(s)

def get_os(os_int):
    if int(os_int) == 1:
        return 'iOS'
    elif int(os_int) == 2:
        return 'android'
    else:
        return ''

