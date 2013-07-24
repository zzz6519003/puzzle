#encoding=utf8
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
            if  project['endDate']:
                endtime = time.strftime( '%Y-%m-%d',time.gmtime(project['endDate']))
            else:
                endtime = ''
            data['project_bug'][pmt_id] = {'pmt_id':pmt_id,
                                        'name':project['projectName'],
                                        'endtime':endtime,
                                        'developer':dev_str,
                                        'qa':qa_str,
                                        'rate':'',
                                        'total':total,
                                        'app':count['app'],
                                        'api':count['api'],
                                        'product':count['product'],
                                        'p1':count['p1'],
                                        'p2':count['p2'],
                                        'p3':count['p3'],
                                        'p4':count['p4'],
                                        'p5':count['p5'],
                                        'test':count['test'],
                                        'dev':count['dev'],
                                        'prerelease':count['prerelease'],
                                        'production':count['production'],
                                        }
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
            
            if  project['endDate']:
                endtime = time.strftime( '%Y-%m-%d',time.gmtime(project['endDate']))
            else:
                endtime = ''
            data['project_bug_reason'][pmt_id]['project']['endtime'] = endtime



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
            data['params'] = {'appName':appName,'category':category,'version':version}

        data['os'] = puzzle_db.select('applist', where = 'appName = $appName',vars = {'appName':appName})
        category = params.get('category')
        version =params.get('version')
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
            if  project['endDate']:
                endtime = time.strftime( '%Y-%m-%d',time.gmtime(project['endDate']))
            else:
                endtime = ''
            data['project_bug_component'][pmt_id]['project']['endtime'] = endtime

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
    owners = puzzle_db.select(table,where ='pmtId = $pmt_id',vars ={'pmt_id':pmt_id})
    return owners


def get_owner_str(owners):
    str = ''
    for owner in owners:
        str += '<span>'+ owner['chinese_name'] +'<br></span>'
    return str

def get_project_list(appName,category,version):
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
    versions = puzzle_db.query("SELECT DISTINCT a.appName as appName ,p.version as version FROM applist AS a,projectlist AS p WHERE a.id = p.appId ORDER BY version")
    for item in versions:
        index = dict_index[item['appName']]
        pos = len(data['version'][index])
        data['version'][index][pos] = item['version']
    return data

