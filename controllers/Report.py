#encoding=utf8
from config import settings
import json
import web 
import string
import time
from model.GlobalFunc import isset

render = settings.render
data = {'pageIndex':'report'}
puzzle_db = settings.puzzle_db
pmt_db = settings.pmt_db
ibug_db = settings.ibug_db

params = web.input()

class Index:
    def GET(self):
        app_id = params.get('app_id')
        version = params.get('version')
        project_list = puzzle_db.select('projectlist',where = 'appId=$app_id AND version = $version',vars = {'app_id':app_id,'version':version})
        data['project_bug'] = {}
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug'][pmt_id] = {}
            data['project_bug'][pmt_id]['count'] = puzzle_db.select('rp_projectbug',where ='pmtId = $pmt_id',vars = {'pmt_id':pmt_id})
        return render.reportIndex(data=data)

class Reason:
    def GET(self):
        app_id = params.get('app_id')
        version = params.get('version')
        reason_all_tmp = ibug_db.select('dd_common',where = "type='reason'",order = 'sort')
        data['th']={}
        for reason in reason_all_tmp:
            id = reason['id']
            data['th'][id] = {'name':reason['name'],'count':0}
        data['th'][0] ={'name':'no reason','count':0}
        
        project_list = puzzle_db.select('projectlist',where = 'appId=$app_id AND version = $version',vars = {'app_id':app_id,'version':version})
        data['project_bug_reason'] = {}
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug_reason'][pmt_id] = {}
            data['project_bug_reason'][pmt_id]['project'] ={}
            data['project_bug_reason'][pmt_id]['reason'] ={}
            
            
            data['project_bug_reason'][pmt_id]['project'] ={'name':project['projectName']}


            project_bug_reason = puzzle_db.select('rp_projectbug_type',where="pmtId = $pmt_id AND type ='reason'",vars = {'pmt_id':pmt_id})
            bug_reason = {}
            for item in project_bug_reason:
                bug_reason[item['com_id']] = item['count']
            

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
        return render.reportReason(data=data)

class Component:
    def GET(self):
        app_id = params.get('app_id')
        version =params.get('version')
        component_all_tmp = ibug_db.select('dd_component')
        data['th'] = {}
        for com in component_all_tmp:
            id = com['int']
            data['th'][id] = {'name':com['name'],'count':0}
        project_list = puzzle_db.select('projectlist',where = 'appId=$app_id AND version = $version',vars = {'app_id':app_id,'version':version})
        data['project_bug_component'] = {}
        for project in project_list:
            pmt_id = project['pmtId']
            data['project_bug_component'][pmt_id] = {}
            data['project_bug_component'][pmt_id]['project'] = {'name':project['projectName']}
            data['project_bug_component'][pmt_id]['component'] ={}
            project_bug_component = puzzle_db.select('rp_projectbug_type',where ="pmtId =$pmt_id AND type='component'",vars = {'pmt_id':pmt_id})
            bug_component = {}
            for item in project_bug_component:
                bug_component[item['com_id']] = item['count']

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
        return render.reportComponent(data=data)

class Update:
    def GET(self):
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
        #获取数据
        return render.reportUpdate(data=data)
