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
from model.GlobalFunc import isset

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
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug'][pmt_id] = {}

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
            data['project_bug'][pmt_id] = count
            data['project_bug'][pmt_id]['pmt_id'] = pmt_id 
            data['project_bug'][pmt_id]['name'] = project['projectName']
            data['project_bug'][pmt_id]['endtime'] = format_time(project['endDate']) 
            data['project_bug'][pmt_id]['developer'] = dev_str
            data['project_bug'][pmt_id]['qa'] = qa_str 
            data['project_bug'][pmt_id]['rate'] = ''
            data['project_bug'][pmt_id]['total'] = total 
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
        data['th'][0] ={'name':'no reason','count':0}
        
        project_list = get_project_list(appName,category,version)
        data['project_bug_reason'] = {}
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug_reason'][pmt_id] = {}
            data['project_bug_reason'][pmt_id]['project'] ={}
            data['project_bug_reason'][pmt_id]['reason'] ={}
            data['project_bug_reason'][pmt_id]['total'] = 0
            data['project_bug_reason'][pmt_id]['project'] ={'name':project['projectName'],'pmt_id':pmt_id}
            devs = get_owners(pmt_id,'dev')
            qas = get_owners(pmt_id,'qa')
            data['project_bug_reason'][pmt_id]['project']['dev'] = get_owner_str(devs)
            data['project_bug_reason'][pmt_id]['project']['qa'] = get_owner_str(qas)
            data['project_bug_reason'][pmt_id]['project']['endtime'] = format_time(project['endDate'])

            project_bug_reason = puzzle_db.select('rp_projectbug_type',where="pmtId = $pmt_id AND type ='reason'",vars = {'pmt_id':pmt_id})
            bug_reason = {}
            for item in project_bug_reason:
                bug_reason[item['com_id']] = item['count']
                data['project_bug_reason'][pmt_id]['total'] += bug_reason[item['com_id']]
            
            for id in data['th']:
                if  id in bug_reason :
                    data['project_bug_reason'][pmt_id]['reason'][id] = bug_reason[id] 
                    data['th'][id]['count'] +=1;
                else:
                    data['project_bug_reason'][pmt_id]['reason'][id] = 0 
        
        for id in data['th'].keys() :
            if data['th'][id]['count'] ==0:
                data['th'].pop(id)
                for pmt_id in data['project_bug_reason']:
                    data['project_bug_reason'][pmt_id]['reason'].pop(id)
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
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug_component'][pmt_id] = {}
            data['project_bug_component'][pmt_id]['project'] = {'name':project['projectName'],'pmt_id':pmt_id}
            devs = get_owners(pmt_id,'dev')
            qas = get_owners(pmt_id,'qa')
            data['project_bug_component'][pmt_id]['project']['dev'] = get_owner_str(devs)
            data['project_bug_component'][pmt_id]['project']['qa'] = get_owner_str(qas)
            data['project_bug_component'][pmt_id]['project']['endtime'] = format_time(project['endDate'])
            data['project_bug_component'][pmt_id]['component'] ={}
            data['project_bug_component'][pmt_id]['total'] = 0
            
            project_bug_component = puzzle_db.select('rp_projectbug_type',where ="pmtId =$pmt_id AND type='component'",vars = {'pmt_id':pmt_id})
            bug_component = {}
            for item in project_bug_component:
                bug_component[item['com_id']] = item['count']
                data['project_bug_component'][pmt_id]['total'] += bug_component[item['com_id']] 

            for id in data['th']:
                if id in bug_component :
                    data['project_bug_component'][pmt_id]['component'][id] = bug_component[id]
                    data['th'][id]['count'] +=1
                else:
                    data['project_bug_component'][pmt_id]['component'][id] = 0
        
        for id in data['th'].keys() :
            if data['th'][id]['count'] == 0:
                data['th'].pop(id)
                for pmt_id in data['project_bug_component']:
                    data['project_bug_component'][pmt_id]['component'].pop(id)
        
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
        for project in project_list:
            pmt_id = project['pmtId']
            users = {}
            devs = get_owners(pmt_id,'dev')
            dev_str = get_owner_str(devs)
            qas = get_owners(pmt_id,'qa')
            qa_str = get_owner_str(qas)
           
            project_info ={}
            project_info['pmt_id'] = pmt_id
            project_info['name'] = project['projectName']
            project_info['endtime'] = format_time(project['endDate'])
            project_info['developer'] = dev_str
            project_info['qa'] = qa_str
            data['data'][pmt_id] ={'project':project_info}

            devs_bug = puzzle_db.select('rp_developer',where="pmtId = $pmt_id",vars={'pmt_id':pmt_id},order='id')
            max_id = 0
            result = {}.fromkeys(('chinese_name','total','workload','workload_div','close','close_div','reject','reopen','lose_repair_div','repair_time','major_bug','repair_time_div','daily_to_rc','daily_to_rc_div'),'')
            for item in devs_bug:
                user_id = item['id']
                total = item['total']
                workload = item['workload']
                user = item
                user['total'] = total
                user['workload_div'] = div(total,workload)
                user['close_div'] = div(user['close'],total)
                user['lose_repair_div'] = div(user['reject']+user['reopen'],total)
                user['repair_time_div'] = div(user['repair_time'],user['major_bug'])
                user['daily_to_rc_div'] = div(user['daily_to_rc'],user['rc'])
                users[user_id] = user
                max_id = user_id
            
            if max_id > 0 :
                total_id = max_id +1
                user_tmp = {}.fromkeys(('total','workload','close','reject','reopen','repair_time','major_bug','daily_to_rc','rc'),0)
                for user_id in users:
                    for key in users[user_id]:
                        if key in user_tmp:
                            user_tmp[key] += users[user_id][key]
                user_tmp['chinese_name'] = 'total'
                total = user_tmp['total']
                user_tmp['workload_div'] = div(total,user_tmp['workload'])
                user_tmp['close_div'] = div(user_tmp['close'],total)
                user_tmp['lose_repair_div'] = div(user_tmp['reject']+user_tmp['reopen'],total)
                user_tmp['repair_time_div'] = div(user_tmp['repair_time'],user_tmp['major_bug'])
                user_tmp['daily_to_rc_div'] = div(user_tmp['daily_to_rc'],user_tmp['rc'])
                user[total_id] = user_tmp
                
                for user_id in users:
                    if user_id != total_id:
                        for key in users[user_id]:
                            if key in result:
                                result[key] += '<span>' + str(users[user_id][key]) + '<br></span>'
                for key in user[total_id]:
                    if key in result:
                        result[key] += '<span>' + str(user[total_id][key]) + '<br></span>'

            data['data'][pmt_id]['count'] = result
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
        for project in project_list:
            pmt_id = project['pmtId']
            
            users = {}

            devs = get_owners(pmt_id,'dev')
            dev_str = get_owner_str(devs)
            qas = get_owners(pmt_id,'qa')
            qa_str = get_owner_str(qas)

            project_info = {}
            project_info['pmt_id'] = pmt_id
            project_info['name'] = project['projectName']
            project_info['endtime'] = format_time(project['endDate'])
            project_info['developer'] = dev_str
            project_info['qa'] = qa_str
            data['data'][pmt_id] ={'project':project_info}

            qas_bug = puzzle_db.select('rp_qa',where = "pmtId = $pmt_id",vars = {'pmt_id':pmt_id},order='id')
            max_id = 0
            result = {}.fromkeys(('total','workload','workload_div','p1','p2','p3','p4','dailybuild','no_dailybuild','dr_div','chinese_name'),'')
            
            for item in qas_bug :
                user_id = item['id']
                total = item['total']
                workload = item['workload']
                user = item
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
                        if key in user_tmp:
                            user_tmp[key] +=  users[user_id][key]
                users[total_id] = user_tmp
                users[total_id]['chinese_name'] = 'total'
                users[total_id]['workload_div'] = div(users[total_id]['total'],users[total_id]['workload'])
                users[total_id]['dr_div'] = div(users[total_id]['dailybuild'],users[total_id]['no_dailybuild'])
                for user_id in users:
                    if user_id != total_id:
                        for key in users[user_id]:
                            if key in result:
                                result[key] += '<span>'+str(users[user_id][key])+'<br><span>'

                for key in users[total_id]:
                    if key in result:                                                             
                        result[key] += '<span>'+str(users[total_id][key])+'<br><span>' 
            data['data'][pmt_id]['count'] = result

        
        return render.reportQa(data=data)

class Update:
    def GET(self):
        params = web.input()
        pmt_id = params.get('pmt_id')
        if not pmt_id :
            raise web.seeother('/index')
        data['pmt_id'] = pmt_id
        value = {'pmt_id':pmt_id}
        #获取当前日期
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()))
        is_update = params.get('is_update')
        data['is_update'] = is_update
        if is_update:
            data['pmt_id'] = pmt_db.select('project',where ='id='+pmt_id)
            data['ticket'] = ibug_db.select('ticket',where ='pmt_id='+pmt_id)

            total = ibug_db.query("SELECT count(id) AS count  FROM ticket "
                                "WHERE pmt_id = $pmt_id AND environment <> 17 "
                                "AND (status <> 'closed' OR status = 'closed' "
                                "AND resolution NOT IN(20,27))",vars = value)[0]['count']
            
            api = ibug_db.query("SELECT count(ticket.id) AS count  FROM ticket,dd_component,dd_common "
                                "WHERE pmt_id = $pmt_id AND environment <> 17 "
                                "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) "
                                "AND ticket.component = dd_component.int AND dd_component.name LIKE '%api%' "
                                "AND ticket.reason = dd_common.id AND dd_common.name NOT LIKE '%产品设计%'",vars = value)[0]['count']


            product = ibug_db.query("SELECT count(ticket.id) AS count  FROM ticket,dd_common "
                                    "WHERE pmt_id = $pmt_id AND environment <> 17 "
                                    "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27))"
                                    "AND ticket.reason = dd_common.id AND dd_common.name LIKE '%产品设计%'",vars = value)[0]['count']
            
            app  = total-api-product

            priorities_tmp = ibug_db.query("SELECT dd_common.name AS name,count(ticket.id) AS count FROM ticket,dd_common "
                                        "WHERE pmt_id = $pmt_id AND environment <>17 "
                                        "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) "
                                        "AND ticket.priority = dd_common.id "
                                        "GROUP BY dd_common.name",vars = value)
            priorities = {'p1':0,'p2':0,'p3':0,'p4':0,'p5':0}
            for priority in  priorities_tmp:
                name = priority['name'].split('-')[0].lower()
                priorities[name] = priority['count']
            
            environments_tmp = ibug_db.query("SELECT dd_common.name AS name,count(ticket.id) AS count FROM ticket,dd_common,dd_component "
                                            "WHERE pmt_id = $pmt_id "
                                            "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                            "AND ticket.environment = dd_common.id "
                                            "AND ticket.component = dd_component.int AND dd_component.name not like '%api%' "
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
       
            reasons_tmp = ibug_db.query("SELECT reason ,count(t.id) AS count  FROM ticket AS t,dd_component AS c "
                                        "WHERE pmt_id = $pmt_id "
                                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND t.component = c.int AND c.name not like '%api%' "
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
            
            component_tmp = ibug_db.query("SELECT component ,count(t.id) as count FROM ticket as t,dd_component as c "
                                        "WHERE pmt_id = $pmt_id "
                                        "AND (status <> 'closed' or status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND t.component = c.int AND c.name not like '%api%' "
                                        "GROUP by component",vars = value)
            puzzle_db.delete("rp_projectbug_type",where = "pmtId = $pmt_id AND type='component'",vars =value)
            for b in component_tmp:
                puzzle_db.insert('rp_projectbug_type',type = 'component',com_id = b['component'],count = b['count'],pmtId = pmt_id ,created =time.time())
            owners = get_owners_from_pmt(pmt_id) 
            devs = owners['dev']
            qas = owners['qa']
            puzzle_db.delete('rp_developer',where = 'pmtId=$pmt_id',vars = value)
            for i in devs:
                user_name = devs[i]['email'].split('@')[0]+'@%'
                dev_value = {'pmt_id':pmt_id,'user_name':user_name}
                dev_count = ibug_db.query("SELECT count(*) AS count FROM ticket AS t,user AS u "
                        "WHERE pmt_id = $pmt_id AND t.environment <>17 "
                        "AND (status<>'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                        "AND t.owner = u.user_name AND email LIKE $user_name",vars=dev_value)[0]['count']
                close = ibug_db.query("SELECT count(*) AS count FROM ticket AS t,user AS u "
                        "WHERE pmt_id = $pmt_id AND t.environment<>17 "
                        "AND status ='closed' AND resolution NOT IN(20,27) "
                        "AND t.owner = u.user_name AND email LIKE $user_name",vars=dev_value)[0]['count']
                reject = ibug_db.query("SELECT count(*)  AS count "
                        "FROM ticket AS t ,ticket_log  AS l ,user AS u "
                        "WHERE pmt_id = $pmt_id AND t.environment<>17 "
                        "AND t.id = l.ticket_id AND l.newvalue = 'opened' "
                        "AND l.field='status' AND l.rlog='Ticket_ActionReject'" 
                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                        "AND t.owner = u.user_name AND u.email LIKE $user_name",vars=dev_value)[0]['count']
                reopen = ibug_db.query("SELECT count(*) AS count "
                        "FROM ticket AS t ,ticket_relation  AS r ,user AS u "
                        "WHERE pmt_id = $pmt_id AND t.environment<>17 AND t.id = r.ticket_id "
                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                        "AND t.owner = u.user_name AND u.email LIKE $user_name",vars=dev_value)[0]['count']
                

                major_bug_all = ibug_db.query("SELECT u.user_name as name,b.id AS id,b.status AS status,b.created_at AS created_at,b.verified_at AS verified_at " 
                        "FROM user AS u,"
                        "(SELECT t.id AS id,t.owner AS owner,t.created_at AS created_at,t.status AS status,MAX(l.created_at) AS verified_at "
                        "FROM ticket AS t "
                        "LEFT JOIN ticket_log AS l "
                        "ON t.id = l.ticket_id "
                        "WHERE t.pmt_id =$pmt_id AND priority IN (6,7,8) "
                        "AND (t.status !='closed' OR t.status ='closed' AND resolution NOT IN(20,27)) "
                        "AND environment <>17 GROUP BY id ) AS b "
                        "WHERE b.owner = u.user_name AND u.email LIKE $user_name",vars = dev_value)
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
                        "FROM ticket AS t ,ticket_log AS l,user AS u "
                        "WHERE  t.id = l.ticket_id AND t.owner=u.user_name "
                        "AND pmt_id=$pmt_id AND environment = 16 "
                        "AND (t.status !='closed' OR t.status ='closed' AND t.resolution NOT IN(20,27)) "
                        "AND l.field='environment' AND l.oldvalue ='Test' AND l.newvalue='Dev' "
                        "AND u.email LIKE $user_name "
                        "GROUP BY t.id",vars =dev_value)
                daily_to_rc = len(test_to_dev)
                rc = ibug_db.query("SELECT count(*) AS count "
                        "FROM ticket AS t ,user AS u "
                        "WHERE t.owner=u.user_name "
                        "AND pmt_id=$pmt_id AND environment = 16 "
                        "AND (t.status !='closed' OR t.status ='closed' AND t.resolution NOT IN(20,27)) "
                        "AND u.email LIKE $user_name ",vars =dev_value)[0]['count']


                puzzle_db.insert('rp_developer',staff_no = devs[i]['staff_no'],chinese_name = devs[i]['chinese_name'],total=dev_count,workload = devs[i]['workload']/8,close=close,reject=reject,reopen=reopen,repair_time=repair_time,major_bug=major_bug,daily_to_rc = daily_to_rc,rc =rc,pmtId =pmt_id)
            puzzle_db.delete('rp_qa',where ='pmtId = $pmt_id',vars = value)
            for i in qas :
                user_name = qas[i]['email'].split('@')[0]+'@%'
                qa_count = ibug_db.query("SELECT count(*) AS count FROM ticket AS t, user AS u "
                                        "WHERE pmt_id = $pmt_id AND reporter = u.user_name "
                                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND email LIKE $user_name",vars={'pmt_id':pmt_id,'user_name':user_name})[0]['count']
                dailybuild = ibug_db.query("SELECT count(*) AS count FROM ticket AS t, user as u "
                                        "WHERE pmt_id = $pmt_id AND reporter = u.user_name "
                                        "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                        "AND email LIKE $user_name AND environment=17",vars={'pmt_id':pmt_id,'user_name':user_name})[0]['count']
                pre_priority = ibug_db.query("SELECT priority,c.name AS name ,count(*) AS count FROM ticket AS t, user as u,dd_common as c "
                                            "WHERE pmt_id = $pmt_id AND reporter = u.user_name "
                                            "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                            "AND email LIKE $user_name AND environment=18 "
                                            "AND t.priority = c.id "
                                            "GROUP BY priority",vars={'pmt_id':pmt_id,'user_name':user_name})
                qa_priority = {'p1':0,'p2':0,'p3':0,'p4':0}
                for priority in  pre_priority:
                    name = priority['name'].split('-')[0].lower()
                    qa_priority[name] = priority['count']


                puzzle_db.insert('rp_qa',staff_no = qas[i]['staff_no'],chinese_name = qas[i]['chinese_name'],total=qa_count,workload = qas[i]['workload']/8,p1=qa_priority['p1'],p2=qa_priority['p2'],p3=qa_priority['p3'],p4=qa_priority['p4'],dailybuild=dailybuild,pmtId =pmt_id)
        #获取数据
        return render.reportUpdate(data=data)


def get_owners_from_pmt(pmt_id):
    dev = {}
    qa = {}
    owners = pmt_db.query("SELECT t.id as owner_id,s.staff_no AS staff_no,s.email as email, t.stage AS stage,SUM(t.workload) AS workload,s.chinese_name AS chinese_name "
                        "FROM task AS t,staff AS s "
                        "WHERE project_id = $pmt_id AND t.owner = s.id "
                        "GROUP BY staff_no",vars ={'pmt_id':pmt_id})
    for owner in owners:
        id = owner['owner_id']
        if owner['stage'] == 107:
            dev[id] = owner
        elif owner['stage'] == 108:
            qa[id] = owner

    return {'dev':dev,'qa':qa}

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
    sql = "SELECT * \
    FROM (SELECT p.id AS id,p.pmtId AS pmtId,p.projectName AS projectName ,\
    p.version AS version,a.appName as appName,a.category AS category \
    FROM projectlist AS p ,applist AS a \
    WHERE p.appId = a.id "
    value ={}
    if appName :
        sql += "AND a.appName = $appName "
        value['appName'] = appName
    if category :
        sql += "AND a.category=$category "
        value['category'] = category
    if version :
        sql += "AND p.version = $version "
        value['version'] = version
    sql += ") as b \
    LEFT JOIN projectevent AS e \
    ON b.id = e.projectId AND e.category =10"
    project_list = puzzle_db.query(sql,vars = value)
    return project_list

def get_select(data):
    data['appName'] = {}
    index = 0
    dict_index = {}
    data['version'] = {}
    appNames = puzzle_db.query("SELECT DISTINCT appName AS appName FROM applist ORDER BY id")
    for item in appNames:
        data['appName'][index] = item['appName']
        dict_index[item['appName']] = index
        data['version'][index] = {}
        index +=1

    versions = puzzle_db.query("SELECT DISTINCT a.appName as appName ,p.version as version \
                                FROM applist AS a,projectlist AS p \
                                WHERE a.id = p.appId ORDER BY version")
    for item in versions:
        index = dict_index[item['appName']]
        pos = len(data['version'][index])
        data['version'][index][pos] = item['version']
    return data

def div(dividend,divisor):
    if divisor ==0:
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
