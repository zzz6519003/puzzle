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
            data['project_bug'][index]['rate'] = ''
            data['project_bug'][index]['total'] = total
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
            data['project_bug_reason'][index]['project'] ={'name':project['appName']+get_os(project['category'])+project['version'],'pmt_id':pmt_id}
            devs = get_owners(pmt_id,'dev')
            qas = get_owners(pmt_id,'qa')
            data['project_bug_reason'][index]['project']['developer'] = get_owner_str(devs)
            data['project_bug_reason'][index]['project']['qa'] = get_owner_str(qas)
            data['project_bug_reason'][index]['project']['endtime'] = format_time(project['endDate'])

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
            data['project_bug_component'][index]['project'] = {'name':project['appName']+get_os(project['category'])+project['version'],'pmt_id':pmt_id}
            devs = get_owners(pmt_id,'dev')
            qas = get_owners(pmt_id,'qa')
            data['project_bug_component'][index]['project']['developer'] = get_owner_str(devs)
            data['project_bug_component'][index]['project']['qa'] = get_owner_str(qas)
            data['project_bug_component'][index]['project']['endtime'] = format_time(project['endDate'])
            data['project_bug_component'][index]['component'] ={}
            data['project_bug_component'][index]['total'] = 0
            
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
        data['params'] = {'appName':appName,'category':category,'version':version}
        
        data['data'] = {}
        project_list = get_project_list(appName,category,version)
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
            project_info['name'] = project['appName']+get_os(project['category'])+project['version']
            project_info['endtime'] = format_time(project['endDate'])
            project_info['developer'] = dev_str
            project_info['qa'] = qa_str
            data['data'][index] ={'project':project_info}

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
                max_id = user_id
            
            if max_id > 0 :
                total_id = max_id +1
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
        data['params'] = {'appName':appName,'category':category,'version':version}
        
        project_list = get_project_list(appName,category,version)
        
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
            project_info['name'] = project['appName']+get_os(project['category'])+project['version']
            project_info['endtime'] = format_time(project['endDate'])
            project_info['developer'] = dev_str
            project_info['qa'] = qa_str
            
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
                max_id = user_id
            
            if max_id > 0:
                total_id = max_id +1
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
                        AND priority  LIKE $priority AND environment !='test'",vars={'pmt_id':pmt_id,'priority':location+'%'})
            elif location in ('test','dev','prerelease','production'):
                tickets = puzzle_db.query("SELECT * FROM ticket \
                        WHERE pmtId=$pmt_id AND component NOT LIKE '%api%' \
                        AND environment=$environment",vars={'pmt_id':pmt_id,'environment':location})
        elif page == 'reason':
            sql = "SELECT * FROM ticket WHERE pmtId=$pmt_id AND component NOT LIKE '%api%' "
            if location =='无原因':
                sql += "AND reason = ''"
            elif location !='total':
                sql += "AND reason = $reason"
            tickets = puzzle_db.query(sql,vars={'pmt_id':urllib.unquote(pmt_id),'reason':location})
        elif page =='component':
            sql = "SELECT * FROM ticket WHERE pmtId=$pmt_id "
            if location !='total':
                sql += "AND component =$component"
            tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'component':urllib.unquote(location)})

        data['tickets'] = tickets
        return render.reportDetail(data=data)



class Update:
    def GET(self):
        params = web.input()
        pmt_id = params.get('pmt_id')
        if pmt_id :
            data['pmt_id'] = pmt_id
        else:
            data['pmt_id'] = ''
        value = {'pmt_id':pmt_id}
        data['success'] = False
        #获取当前日期
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))
        is_update = params.get('is_update')
        data['is_update'] = is_update
        if pmt_id and is_update:
            data['ticket'] = ibug_db.select('ticket',where ='pmt_id='+pmt_id)
            puzzle_db.delete('ticket',where ='pmtId='+pmt_id)
            ticket_detail = ibug_db.query("SELECT t.resolution,t.id AS ticket_id,created_at , \
                    updated_at,closed_at,p.name AS priority,\
                    r.chinese_name AS reporter,o.chinese_name AS owner,\
                    status,summary,pmt_id,e.name AS environment ,\
                    c.name AS component,re.name AS resolution,rea.name AS reason \
                    FROM ticket AS t \
                    LEFT JOIN dd_common AS p \
                    ON t.priority=p.id \
                    LEFT JOIN user AS r \
                    ON t.reporter =r.user_name \
                    LEFT JOIN user AS o \
                    ON t.owner = o.user_name \
                    LEFT JOIN dd_common AS e \
                    ON t.environment =e.id \
                    LEFT JOIN dd_component AS c \
                    ON t.component = c.int \
                    LEFT JOIN dd_common AS re \
                    ON t.resolution = re.id \
                    LEFT JOIN dd_common AS rea \
                    ON t.reason = rea.id \
                    WHERE pmt_id = $pmt_id \
                    AND (status <>'closed' OR status='closed' AND t.resolution NOT IN(20,27))",vars=value)
            for item in ticket_detail:
                if not item['resolution']:
                    item['resolution'] =''
                if not item['reason']:
                    item['reason'] = ''
                is_reject = 0
                is_reopen = 0
                is_daily_to_rc = 0
                reject_tmp = ibug_db.query("SELECT * FROM ticket_log \
                        WHERE ticket_id=$ticket_id AND field='status' \
                        AND rlog='Ticket_ActionReject'",vars={'ticket_id':item['ticket_id']})
                if len(reject_tmp) > 0:
                    is_reject = 1
                reopen_tmp = ibug_db.query("SELECT * FROM ticket_relation WHERE ticket_id =$ticket_id",vars={'ticket_id':item['ticket_id']})
                if len(reopen_tmp) >0:
                    is_reopen = 1

                if item['environment'] =='Dev':
                    daily_to_rc_tmp = ibug_db.query("SELECT * FROM ticket_log WHERE ticket_id=$ticket_id AND field='environment' AND oldvalue='Test' AND newvalue='Dev'",vars={'ticket_id':item['ticket_id']})
                    if len(daily_to_rc_tmp) > 0:
                        is_daily_to_rc = 1



                puzzle_db.insert('ticket',ticket_id=item['ticket_id'],created_at=item['created_at'],updated_at=item['updated_at'],closed_at=item['closed_at'],priority=item['priority'],reporter=item['reporter'],owner=item['owner'],status=item['status'],summary=item['summary'],pmtId=item['pmt_id'],environment=item['environment'],component=item['component'],resolution=item['resolution'],reason=item['reason'],is_reopen=is_reopen,is_reject=is_reject,is_daily_to_rc=is_daily_to_rc)
            total = ibug_db.query("SELECT count(id) AS count  FROM ticket "
                                "WHERE pmt_id = $pmt_id AND environment <> 17 "
                                "AND (status <> 'closed' OR status = 'closed' "
                                "AND resolution NOT IN(20,27))",vars = value)[0]['count']
            
            api = ibug_db.query("SELECT count(*) AS count FROM ticket \
                    LEFT JOIN dd_component \
                    ON ticket.component = dd_component.int \
                    LEFT JOIN dd_common \
                    ON ticket.reason = dd_common.id \
                    WHERE pmt_id = $pmt_id AND environment <> 17 \
                    AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) \
                    AND dd_component.name LIKE '%api%' AND dd_common.name NOT LIKE '%产品设计%'",vars = value)[0]['count']


            product = ibug_db.query("SELECT count(ticket.id) AS count  FROM ticket "
                                    "LEFT JOIN dd_common "
                                    "ON ticket.reason = dd_common.id "
                                    "WHERE pmt_id = $pmt_id AND environment <> 17 "
                                    "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) "
                                    "AND dd_common.name LIKE '%产品设计%'",vars = value)[0]['count']
            
            app  = total-api-product

            priorities_tmp = ibug_db.query("SELECT dd_common.name AS name,count(ticket.id) AS count FROM ticket "
                                        "LEFT JOIN dd_common "
                                        "ON ticket.priority = dd_common.id "
                                        "LEFT JOIN dd_component "
                                        "ON ticket.component = dd_component.int "
                                        "WHERE pmt_id = $pmt_id AND environment <>17 "
                                        "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) "
                                        "AND dd_component.name not like '%api%' "
                                        "GROUP BY dd_common.name",vars = value)
            priorities = {'p1':0,'p2':0,'p3':0,'p4':0,'p5':0}
            for priority in  priorities_tmp:
                name = priority['name'].split('-')[0].lower()
                priorities[name] = priority['count']
            
            environments_tmp = ibug_db.query("SELECT dd_common.name AS name,count(ticket.id) AS count FROM ticket "
                                            "LEFT JOIN dd_common "
                                            "ON ticket.environment = dd_common.id "
                                            "LEFT JOIN dd_component "
                                            "ON ticket.component = dd_component.int "
                                            "WHERE pmt_id = $pmt_id "
                                            "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                            "AND dd_component.name not like '%api%' "
                                            "GROUP BY dd_common.name",vars = value)

            
            environments = {'test':0,'dev':0,'prerelease':0,'production':0}
            for environment in environments_tmp:
                name = environment['name'].lower()
                environments[name] = environment['count']

            project_bug = puzzle_db.select('rp_projectbug',where = 'pmtId = $pmt_id',vars = value)
            if len(project_bug):
                puzzle_db.update('rp_projectbug',where = 'pmtId = $pmt_id',vars = value, app = app, api = api , product = product , p1 = priorities['p1'] , p2 = priorities['p2'] ,  p3 = priorities['p3'] ,  p4 = priorities['p4'] , p5 = priorities['p5'] , test = environments['test'] ,dev = environments['dev'] ,prerelease = environments['prerelease'] , production = environments['production'])
            else:
                puzzle_db.insert('rp_projectbug', app = app, api = api , product = product , p1 = priorities['p1'] , p2 = priorities['p2'] ,  p3 = priorities['p3'] ,  p4 = priorities['p4'] , p5 = priorities['p5'] , test = environments['test'] ,dev = environments['dev'] ,prerelease = environments['prerelease'] , production = environments['production'], pmtId = pmt_id, created = time.time())
       
            reasons_tmp = ibug_db.query("SELECT reason ,count(*) AS count  FROM ticket AS t "
                                        "LEFT JOIN dd_component AS c "
                                        "ON component = c.int "
                                        "WHERE pmt_id = $pmt_id "
                                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND c.name not like '%api%' "
                                        "GROUP BY reason",vars = value)
            
            puzzle_db.delete("rp_projectbug_type",where = "pmtId =$pmt_id AND type = 'reason'",vars = value)
            reason = {}
            data['test'] = {}
            for a in reasons_tmp:
                if not a['reason'].isdigit():
                    id = 0
                else:
                    id = a['reason']
                if id in reason:
                    reason[id]['count'] = reason[id]['count'] +a['count']
                else:
                    reason[id] = {'count':a['count']}


            for reason_id in reason:
                puzzle_db.insert('rp_projectbug_type',type ='reason',com_id = reason_id,count = reason[reason_id]['count'],pmtId = pmt_id,created = time.time())
            
            component_tmp = ibug_db.query("SELECT component ,count(t.id) AS count FROM ticket AS t "
                                        "LEFT JOIN dd_component AS c "
                                        "ON t.component = c.int "
                                        "WHERE pmt_id = $pmt_id "
                                        "AND (status <> 'closed' or status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND c.name not like '%api%' "
                                        "GROUP by component",vars = value)
            puzzle_db.delete("rp_projectbug_type",where = "pmtId = $pmt_id AND type='component'",vars =value)
            for b in component_tmp:
                puzzle_db.insert('rp_projectbug_type',type = 'component',com_id = b['component'],count = b['count'],pmtId = pmt_id ,created =time.time())
            
            #dev,qa模块
            task_owners = get_task_owners_from_pmt(pmt_id) 
            ticket_owners = get_ticket_owners_from_ibug(pmt_id)
            data['users'] = ticket_owners
            devs = get_compose_users(task_owners['dev'],ticket_owners)
            ticket_reporters = get_ticket_reporters_from_ibug(pmt_id)
            qas =get_compose_users(task_owners['qa'],ticket_reporters)
            puzzle_db.delete('rp_developer',where = 'pmtId=$pmt_id',vars = value)
            pmt_to_ibug_user_sql = ' AND chinese_name =$chinese_name '
            for i in devs:
                #user_name = devs[i]['email'].split('@')[0]+'@%'
                chinese_name = devs[i]['chinese_name']
                dev_value = {'pmt_id':pmt_id,'chinese_name':chinese_name}
                dev_count = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                        "LEFT JOIN user AS u "
                        "ON t.owner = u.user_name "
                        "WHERE pmt_id = $pmt_id AND t.environment <>17 "
                        "AND (status<>'closed' OR status ='closed' "
                        "AND resolution NOT IN(20,27)) "+ pmt_to_ibug_user_sql,vars=dev_value)[0]['count']
                unclose = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                        "LEFT JOIN user AS u "
                        "ON t.owner = u.user_name "
                        "WHERE pmt_id = $pmt_id AND t.environment<>17 "
                        "AND status <>'closed' AND resolution NOT IN(20,27) "
                        + pmt_to_ibug_user_sql,vars=dev_value)[0]['count']
                reject = ibug_db.query("SELECT count(*)  AS count "
                        "FROM ticket AS t "
                        "LEFT JOIN ticket_log  AS l "
                        "ON t.id =l.ticket_id "
                        "LEFT JOIN user AS u "
                        "ON owner = u.user_name "
                        "WHERE pmt_id = $pmt_id AND t.environment<>17 "
                        "AND l.newvalue = 'opened' "
                        "AND l.field='status' AND l.rlog='Ticket_ActionReject'" 
                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                        + pmt_to_ibug_user_sql,vars=dev_value)[0]['count']
                reopen = ibug_db.query("SELECT count(*) AS count "
                        "FROM ticket AS t "
                        "LEFT JOIN ticket_relation  AS r "
                        "ON t.id =r.ticket_id "
                        "LEFT JOIN user AS u "
                        "ON owner = u.user_name "
                        "WHERE pmt_id = $pmt_id AND t.environment<>17 AND r.ticket_id is not null "
                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                        +pmt_to_ibug_user_sql,vars=dev_value)[0]['count']
                

                major_bug_all = ibug_db.query("SELECT user_name as name,b.id AS id,b.status AS status,b.created_at AS created_at,b.verified_at AS verified_at " 
                        "FROM user AS u"
                        "LEFT JOIN (SELECT t.id AS id,t.owner AS owner,t.created_at AS created_at,t.status AS status,MAX(l.created_at) AS verified_at "
                        "FROM ticket AS t "
                        "LEFT JOIN ticket_log AS l "
                        "ON t.id = l.ticket_id "
                        "WHERE t.pmt_id =$pmt_id AND priority IN (6,7,8) "
                        "AND (t.status !='closed' OR t.status ='closed' AND resolution NOT IN(20,27)) "
                        "AND environment <>17 GROUP BY id ) AS b "
                        "ON b.owner = user_name "+ pmt_to_ibug_user_sql,vars = dev_value)
                major_bug = len(major_bug_all)
                repair_time = 0
                aday = 3600*24
                for item in major_bug_all:
                    created = datetime_to_timestamp(item['created_at'])
                    if item['status']=='closed':
                        end = datetime_to_timestamp(item['verified_at'])
                    else:
                        end = int(time.time())
                    repair_time += end -created
                repair_time = repair_time/aday
                
                test_to_dev = ibug_db.query("SELECT t.id,MAX(l.created_at) "
                        "FROM ticket AS t "
                        "LEFT JOIN ticket_log AS l "
                        "ON t.id = l.ticket_id "
                        "LEFT JOIN user AS u "
                        "ON owner=u.user_name "
                        "WHERE  t.id = l.ticket_id "
                        "AND pmt_id=$pmt_id AND environment = 16 "
                        "AND (t.status !='closed' OR t.status ='closed' AND t.resolution NOT IN(20,27)) "
                        "AND l.field='environment' AND l.oldvalue ='Test' AND l.newvalue='Dev' "
                        + pmt_to_ibug_user_sql+
                        "GROUP BY t.id",vars =dev_value)
                daily_to_rc = len(test_to_dev)
                rc = ibug_db.query("SELECT count(*) AS count "
                        "FROM ticket AS t "
                        "LEFT JOIN user AS u "
                        "ON t.owner = u.user_name "
                        "WHERE t.owner=u.user_name "
                        "AND pmt_id=$pmt_id AND environment = 16 "
                        "AND (t.status !='closed' OR t.status ='closed' AND t.resolution NOT IN(20,27)) "
                        + pmt_to_ibug_user_sql,vars =dev_value)[0]['count']

                puzzle_db.insert('rp_developer',staff_no = devs[i]['staff_no'],chinese_name = devs[i]['chinese_name'],total=dev_count,workload = devs[i]['workload']/8,unclose=unclose,reject=reject,reopen=reopen,repair_time=repair_time,major_bug=major_bug,daily_to_rc = daily_to_rc,rc =rc,user_from=devs[i]['from'],pmtId =pmt_id)
            
            puzzle_db.delete('rp_qa',where ='pmtId = $pmt_id',vars = value)
            for i in qas :
                #user_name = qas[i]['email'].split('@')[0]+'@%'
                qa_value = {'pmt_id':pmt_id,'chinese_name':qas[i]['chinese_name']}
                qa_count = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                                        "LEFT JOIN user AS u "
                                        "ON reporter = u.user_name "
                                        "WHERE pmt_id = $pmt_id "
                                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                        + pmt_to_ibug_user_sql,vars=qa_value)[0]['count']
                dailybuild = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                                        "LEFT JOIN user as u "
                                        "ON reporter = u.user_name "
                                        "WHERE pmt_id = $pmt_id "
                                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND environment=17 "+ pmt_to_ibug_user_sql,vars=qa_value)[0]['count']
                pre_priority = ibug_db.query("SELECT priority,c.name AS name ,count(*) AS count FROM ticket AS t"
                                            "LEFT JOIN user as u "
                                            "ON reporter = u.user_name "
                                            "LEFT JOIN dd_common as c "
                                            "ON priority = c.id "
                                            "WHERE pmt_id = $pmt_id "
                                            "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                            "AND environment=18 "+ pmt_to_ibug_user_sql+
                                            "GROUP BY priority",vars = qa_value)
                qa_priority = {'p1':0,'p2':0,'p3':0,'p4':0}
                for priority in  pre_priority:
                    name = priority['name'].split('-')[0].lower()
                    qa_priority[name] = priority['count']


                puzzle_db.insert('rp_qa',staff_no = qas[i]['staff_no'],chinese_name = qas[i]['chinese_name'],total=qa_count,workload = qas[i]['workload']/8,p1=qa_priority['p1'],p2=qa_priority['p2'],p3=qa_priority['p3'],p4=qa_priority['p4'],dailybuild=dailybuild,user_from=qas[i]['from'],pmtId =pmt_id)
                data['success'] = True
        #获取数据
        return render.reportUpdate(data=data)





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
        tickets = puzzle_db.select('ticket', where="pmtId=$pmt_id AND environment !='test' AND component NOT LIKE '%api%'",vars ={'pmt_id':pmt_id})
    else:
        tickets = puzzle_db.select('ticket', where=" pmtId=$pmt_id AND owner = $cn_name AND environment !='test'",vars ={'pmt_id':pmt_id,'cn_name':cn_name})
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
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id AND is_reject=1 AND environment!='test' "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets


def get_dev_reopen_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id AND is_reopen=1 AND environment!='test' "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets

def get_dev_daily_to_rc_bugs_from_puzzle(pmt_id,cn_name):
    sql = "SELECT * FROM ticket WHERE pmtId = $pmt_id  AND is_daily_to_rc=1 "
    if cn_name !='total':
        sql += " AND owner = $cn_name"
    else:
        sql +=" AND component NOT LIKE '%api%'"
    tickets = puzzle_db.query(sql,vars={'pmt_id':pmt_id,'cn_name':cn_name})
    return tickets



def filter_project_info(fl_project,project,dev_str,qa_str):
    fl_project['pmt_id'] = project['pmtId']
    fl_project['name'] = project['appName']+get_os(project['category'])+project['version']
    fl_project['endtime'] = format_time(project['endDate']) 
    fl_project['developer'] = dev_str
    fl_project['qa'] = qa_str

    return fl_project




def get_task_owners_from_pmt(pmt_id):
    dev = {}
    qa = {}
    owners = pmt_db.query("SELECT s.staff_no AS staff_no,s.email AS email, t.stage AS stage,SUM(t.workload) AS workload,s.chinese_name AS chinese_name "
                        "FROM task AS t,staff AS s "
                        "WHERE project_id = $pmt_id AND t.owner = s.id "
                        "GROUP BY staff_no",vars ={'pmt_id':pmt_id})
    for owner in owners:
        if owner['stage'] == 107:
            id = len(dev)
            dev[id] = owner
            dev[id]['from'] = 1
        elif owner['stage'] == 108:
            id = len(qa)
            qa[id] = owner
            qa[id]['from'] = 1

    return {'dev':dev,'qa':qa}

def get_ticket_owners_from_ibug(pmt_id):
    owners = {}
    owners_tmp = ibug_db.query("SELECT distinct u.user_name,u.chinese_name AS chinese_name,u.email AS email \
            FROM ticket AS t \
            LEFT JOIN user AS u \
            ON t.owner = u.user_name \
            LEFT JOIN dd_component AS c \
            ON t.component = c.int \
            WHERE pmt_id =$pmt_id AND environment<>17 \
            AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) \
            AND c.name not like '%api%'",vars={'pmt_id':pmt_id})
    for owner in owners_tmp:
        #user = owner['email'].split('@')[0]
        value ={'chinese_name':owner['chinese_name']}
        tmp = get_user_from_pmt(value)
        if len(tmp) > 0:
            id = len(owners)
            owners[id] ={'workload':0,'from':2}
            user_tmp = tmp[0]
            for key in user_tmp:
                owners[id][key] = user_tmp[key]

    return owners

def get_ticket_reporters_from_ibug(pmt_id):
    reporters = {}
    reporters_tmp = ibug_db.query("SELECT distinct u.user_name,u.chinese_name AS chinese_name,u.email AS email FROM ticket AS t  \
            LEFT JOIN user AS u \
            ON t.reporter = u.user_name \
            WHERE pmt_id =$pmt_id  \
            AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27))",vars={'pmt_id':pmt_id})
    for reporter in reporters_tmp:  
        #user = reporter['email'].split('@')[0]
        value ={'chinese_name':reporter['chinese_name']}
        tmp = get_user_from_pmt(value)
        if len(tmp) > 0:      
            id = len(reporters)      
            reporters[id] ={'workload':0,'from':2} 
            user_tmp = tmp[0] 
            for key in user_tmp:               
                reporters[id][key] = user_tmp[key]

    return reporters

def get_user_from_pmt(value):
    tmp = pmt_db.query("SELECT staff_no,email,chinese_name \
            FROM staff \
            WHERE chinese_name=$chinese_name \
            ORDER BY id DESC ",vars=value)
    return tmp


def get_compose_users(pmt,ibug):
    for i in ibug:
        res = False
        for j in pmt:
            if pmt[j]['email']  == ibug[i]['email']:
                res = True
        if res == False :
            id = len(pmt)
            pmt[id] = ibug[i]
    return pmt


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
        str += '<span>'+ owner['chinese_name'] +'<br></span>'
    return str

def get_project_list(appName,category,version):
    if not appName and not category and not version:
        return {}
    sql = "SELECT b.pmtId AS pmtId,b.projectName AS projectName,b.version AS version,\
    b.appName AS appName,b.category AS category,e.endDate AS endDate \
    FROM (SELECT p.id AS id,p.pmtId AS pmtId,p.projectName AS projectName ,\
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
    ON b.id = e.projectId AND e.category =10 ORDER BY pmtId DESC"
    project_list = puzzle_db.query(sql,vars = value)
    return project_list

def get_select(data):
    data['appName'] = {}
    index = 0
    dict_index = {}
    data['version'] = {}
    appNames = puzzle_db.query("SELECT DISTINCT appGroup AS appName FROM applist ORDER BY id")
    for item in appNames:
        data['appName'][index] = item['appName']
        dict_index[item['appName']] = index
        data['version'][index] = {}
        index +=1

    versions = puzzle_db.query("SELECT DISTINCT a.appGroup as appName ,p.version as version \
                                FROM applist AS a,projectlist AS p \
                                WHERE a.id = p.appId ORDER BY version")
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

def format_time(timestamp):
    import time
    if timestamp :
        format_time = time.strftime( '%Y-%m-%d',time.gmtime(timestamp))
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

