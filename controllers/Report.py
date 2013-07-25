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
            data['data'][pmt_id] = {}.fromkeys(('total','workload','workload_div','p1','p2','p3','p4','dailybuild','no_dailybuild','dr_div','chinese_name'),'')

            devs = get_owners(pmt_id,'dev')
            dev_str = get_owner_str(devs)
            qas = get_owners(pmt_id,'qa')
            qa_str = get_owner_str(qas)
            
            qas_bug = puzzle_db.select('rp_qa',where = "pmtId = $pmt_id",vars = {'pmt_id':pmt_id},order='user_id')
            max_id = 0
            for item in qas_bug :
                user_id = item['user_id']
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
                            if key in data['data'][pmt_id]:
                                data['data'][pmt_id][key] += '<span>'+str(users[user_id][key])+'<br><span>'

                for key in users[total_id]:
                    if key in data['data'][pmt_id]:                                                             
                        data['data'][pmt_id][key] += '<span>'+str(users[total_id][key])+'<br><span>' 

            data['data'][pmt_id]['pmt_id'] = pmt_id
            data['data'][pmt_id]['name'] = project['projectName']
            data['data'][pmt_id]['endtime'] = format_time(project['endDate'])
            data['data'][pmt_id]['developer'] = dev_str
            data['data'][pmt_id]['qa'] = qa_str
        
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
                puzzle_db.insert('rp_developer',user_id = devs[i]['owner_id'],chinese_name = devs[i]['chinese_name'],workload = devs[i]['workload']/8,pmtId =pmt_id)
            puzzle_db.delete('rp_qa',where ='pmtId = $pmt_id',vars = value)
            for i in qas :
                puzzle_db.insert('rp_qa',user_id = qas[i]['owner_id'],chinese_name = qas[i]['chinese_name'],workload = qas[i]['workload']/8,pmtId =pmt_id)
        #获取数据
        return render.reportUpdate(data=data)


def get_owners_from_pmt(pmt_id):
    dev = {}
    qa = {}
    owners = pmt_db.query("SELECT t.owner AS owner_id, t.stage AS stage,SUM(t.workload) AS workload,s.chinese_name AS chinese_name "
                        "FROM task AS t,staff AS s "
                        "WHERE project_id = $pmt_id AND t.owner = s.id "
                        "GROUP BY owner_id",vars ={'pmt_id':pmt_id})
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
    owners = puzzle_db.select(table,where ='pmtId = $pmt_id',vars ={'pmt_id':pmt_id},order ='user_id')
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
        return ''
    else :
        return round(dividend/divisor,1)

def format_time(timestamp):
    import time
    if timestamp :
        format_time = time.strftime( '%Y-%m-%d',time.gmtime(timestamp))
    else :
        format_time = ''
    return format_time
