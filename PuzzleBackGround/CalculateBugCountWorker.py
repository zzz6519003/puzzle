#!/usr/bin/python
#encoding=utf8
import json
import sys
import web

reload(sys)
sys.setdefaultencoding('utf8')
import os
import datetime

import time
import settings
#path = "%s/model" % os.getcwd()
sys.path.append("../model")
from GlobalFunc import send_mail

data = {}

def doWork(gearmanWorker, job):
    puzzle_db = settings.getConnectionV2('puzzle')
    pmt_db = settings.getConnectionV2('pmt')
    ibug_db = settings.getConnectionV2('ibug')

    params = json.loads(job.data)
    pmt_id = params['pmt_id']

    value = {'pmt_id': pmt_id}
    try:
        error = ""
        data['ticket'] = ibug_db.select('ticket', where='pmt_id=' + pmt_id)
        puzzle_db.delete('ticket', where='pmtId=' + pmt_id)
        error = "================ticket start===============<br>"
        ticket_detail = ibug_db.query("SELECT t.resolution,t.id AS ticket_id,created_at ,person_liable, \
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
                    AND (status <>'closed' OR status='closed' AND t.resolution NOT IN(20,27))", vars=value)
        for item in ticket_detail:
            if not item['resolution']:
                item['resolution'] = ''
            if not item['reason']:
                item['reason'] = ''
            is_reject = 0
            is_reopen = 0
            is_daily_to_rc = 0
            reject_tmp = ibug_db.query("SELECT * FROM ticket_log \
                        WHERE ticket_id=$ticket_id AND field='status' \
                        AND rlog='Ticket_ActionReject'", vars={'ticket_id': item['ticket_id']})
            if len(reject_tmp) > 0:
                is_reject = 1
            reopen_tmp = ibug_db.query("SELECT * FROM ticket_relation WHERE ticket_id =$ticket_id",
                                       vars={'ticket_id': item['ticket_id']})
            if len(reopen_tmp) > 0:
                is_reopen = 1

            if item['environment'] == 'Dev':
                daily_to_rc_tmp = ibug_db.query(
                    "SELECT * FROM ticket_log WHERE ticket_id=$ticket_id AND field='environment' AND oldvalue='Test' AND newvalue='Dev'",
                    vars={'ticket_id': item['ticket_id']})
                if len(daily_to_rc_tmp) > 0:
                    is_daily_to_rc = 1
            puzzle_db.insert('ticket', ticket_id=item['ticket_id'], created_at=item['created_at'],
                             updated_at=item['updated_at'], closed_at=item['closed_at'], priority=item['priority'],
                             reporter=item['reporter'], owner=item['owner'], status=item['status'],
                             summary=item['summary'], pmtId=item['pmt_id'], environment=item['environment'],
                             component=item['component'], resolution=item['resolution'], reason=item['reason'],
                             person_liable=item['person_liable'],is_reopen=is_reopen, is_reject=is_reject, is_daily_to_rc=is_daily_to_rc)
        error += "================ticket end===============<br>"
        error += "================project start===============<br>"

        total = ibug_db.query("SELECT count(id) AS count  FROM ticket "
                              "WHERE pmt_id = $pmt_id AND environment <> 17 "
                              "AND (status <> 'closed' OR status = 'closed' "
                              "AND resolution NOT IN(20,27))", vars=value)[0]['count']

        api = ibug_db.query("SELECT count(distinct ticket.id)  AS count FROM ticket \
                    LEFT JOIN dd_component \
                    ON ticket.component = dd_component.int \
                    LEFT JOIN dd_common \
                    ON (ticket.reason ='' OR ticket.reason = dd_common.id ) \
                    WHERE pmt_id = $pmt_id AND environment <> 17 \
                    AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) \
                    AND dd_component.name LIKE '%api%' AND dd_common.name NOT LIKE '%产品设计%'", vars=value)[0]['count']

        product = ibug_db.query("SELECT count(*) AS count  FROM ticket "
                                "LEFT JOIN dd_common "
                                "ON  ticket.reason = dd_common.id  "
                                "WHERE pmt_id = $pmt_id AND environment <> 17 "
                                "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) "
                                "AND dd_common.name LIKE '%产品设计%'", vars=value)[0]['count']

        app = total - api - product

        priorities_tmp = ibug_db.query("SELECT dd_common.name AS name,count(ticket.id) AS count FROM ticket "
                                       "LEFT JOIN dd_common "
                                       "ON ticket.priority = dd_common.id "
                                       "LEFT JOIN dd_common AS d "
                                       "ON ticket.reason = d.id "
                                       "LEFT JOIN dd_component "
                                       "ON ticket.component = dd_component.int "
                                       "WHERE pmt_id = $pmt_id AND environment <>17 "
                                       "AND (status <> 'closed' OR status = 'closed' AND resolution NOT IN(20,27)) "
                                       "AND dd_component.name not like '%api%' AND (d.name is null or d.name not like '%产品设计%') "
                                       "GROUP BY dd_common.name", vars=value)
        priorities = {'p1': 0, 'p2': 0, 'p3': 0, 'p4': 0, 'p5': 0}
        for priority in priorities_tmp:
            name = priority['name'].split('-')[0].lower()
            priorities[name] = priority['count']

        environments_tmp = ibug_db.query("SELECT dd_common.name AS name,count(ticket.id) AS count FROM ticket "
                                         "LEFT JOIN dd_common "
                                         "ON ticket.environment = dd_common.id "
                                         "LEFT JOIN dd_common AS d "
                                         "ON ticket.reason = d.id "
                                         "LEFT JOIN dd_component "
                                         "ON ticket.component = dd_component.int "
                                         "WHERE pmt_id = $pmt_id "
                                         "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                         "AND dd_component.name not like '%api%' AND (d.name is null or d.name not like '%产品设计%') "
                                         "GROUP BY dd_common.name", vars=value)

        environments = {'test': 0, 'dev': 0, 'prerelease': 0, 'production': 0}
        for environment in environments_tmp:
            name = environment['name'].lower()
            environments[name] = environment['count']

        project_bug = puzzle_db.select('rp_projectbug', where='pmtId = $pmt_id', vars=value)
        if len(project_bug):
            puzzle_db.update('rp_projectbug', where='pmtId = $pmt_id', vars=value, app=app, api=api,
                             product=product, p1=priorities['p1'], p2=priorities['p2'], p3=priorities['p3'],
                             p4=priorities['p4'], p5=priorities['p5'], test=environments['test'],
                             dev=environments['dev'], prerelease=environments['prerelease'],
                             production=environments['production'])
        else:
            puzzle_db.insert('rp_projectbug', app=app, api=api, product=product, p1=priorities['p1'],
                             p2=priorities['p2'], p3=priorities['p3'], p4=priorities['p4'], p5=priorities['p5'],
                             test=environments['test'], dev=environments['dev'],
                             prerelease=environments['prerelease'], production=environments['production'],
                             pmtId=pmt_id)

        error += "================project end===============<br>"
        error += "================reason start===============<br>"


        reasons_tmp = ibug_db.query("SELECT reason ,count(*) AS count  FROM ticket AS t "
                                    "LEFT JOIN dd_common AS d "
                                    "ON t.reason = d.id "
                                    "LEFT JOIN dd_component AS c "
                                    "ON component = c.int "
                                    "WHERE pmt_id = $pmt_id "
                                    "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                    "AND c.name not like '%api%' AND (d.name is null or d.name not like '%产品设计%')  "
                                    "GROUP BY reason", vars=value)

        puzzle_db.delete("rp_projectbug_type", where="pmtId =$pmt_id AND type = 'reason'", vars=value)
        reason = {}
        for a in reasons_tmp:
            if not a['reason'].isdigit():
                id = 0
            else:
                id = a['reason']
            if id in reason:
                reason[id]['count'] = reason[id]['count'] + a['count']
            else:
                reason[id] = {'count': a['count']}

        for reason_id in reason:
            puzzle_db.insert('rp_projectbug_type', type='reason', com_id=reason_id,
                             count=reason[reason_id]['count'], pmtId=pmt_id)
        error += "================component start===============<br>"

        component_tmp = ibug_db.query("SELECT component ,count(t.id) AS count FROM ticket AS t "
                                      "LEFT JOIN dd_common AS d "
                                      "ON t.reason = d.id "
                                      "LEFT JOIN dd_component AS c "
                                      "ON t.component = c.int "
                                      "WHERE pmt_id = $pmt_id "
                                      "AND (status <> 'closed' or status ='closed' AND resolution NOT IN(20,27)) "
                                      "AND c.name not like '%api%' AND  (d.name is null or d.name not like '%产品设计%')  "
                                      "GROUP by component", vars=value)
        puzzle_db.delete("rp_projectbug_type", where="pmtId = $pmt_id AND type='component'", vars=value)
        for b in component_tmp:
            puzzle_db.insert('rp_projectbug_type', type='component', com_id=b['component'], count=b['count'],
                             pmtId=pmt_id)
        error += "================dev start===============<br>"

        #dev,qa模块
        task_owners = get_task_owners_from_pmt(pmt_db,pmt_id)
        ticket_owners = get_ticket_person_liable_from_ibug(pmt_db,ibug_db,pmt_id)
        devs = get_compose_users(task_owners['dev'], ticket_owners)
        data['devs'] = ticket_owners
        ticket_reporters = get_ticket_reporters_from_ibug(pmt_db,ibug_db,pmt_id)
        qas = get_compose_users(task_owners['qa'], ticket_reporters)

        puzzle_db.delete('rp_developer', where='pmtId=$pmt_id', vars=value)
        pmt_to_ibug_user_sql = ' AND person_liable like $chinese_name '
        for i in devs:
            #user_name = devs[i]['email'].split('@')[0]+'@%'
            chinese_name = devs[i]['chinese_name']
            dev_value = {'pmt_id': pmt_id, 'chinese_name':chinese_name+'%'}
            dev_count = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                                      "LEFT JOIN dd_common AS d "
                                      "ON t.reason = d.id "
                                      "WHERE pmt_id = $pmt_id AND t.environment <>17 "
                                      "AND (status<>'closed' OR status ='closed' "
                                      "AND resolution NOT IN(20,27)) AND (d.name is null or d.name not like '%产品设计%') " + pmt_to_ibug_user_sql,
                                      vars=dev_value)[0][
                'count']
            unclose = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                                    "WHERE pmt_id = $pmt_id AND t.environment<>17 "
                                    "AND status <>'closed' AND resolution NOT IN(20,27) "
                                    + pmt_to_ibug_user_sql, vars=dev_value)[0]['count']
            reject = ibug_db.query("SELECT count(*)  AS count "
                                   "FROM ticket AS t "
                                   "LEFT JOIN dd_common AS d "
                                   "ON t.reason = d.id "
                                   "LEFT JOIN ticket_log  AS l "
                                   "ON t.id =l.ticket_id "
                                   "WHERE pmt_id = $pmt_id AND t.environment<>17 "
                                   "AND l.newvalue = 'opened' "
                                   "AND l.field='status' AND l.rlog='Ticket_ActionReject'"
                                   "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                   "AND (d.name is null or d.name not like '%产品设计%') "
                                   + pmt_to_ibug_user_sql, vars=dev_value)[0]['count']
            reopen = ibug_db.query("SELECT count(*) AS count "
                                   "FROM ticket AS t "
                                   "LEFT JOIN dd_common AS d "
                                   "ON t.reason = d.id "
                                   "LEFT JOIN ticket_relation  AS r "
                                   "ON t.id =r.ticket_id "
                                   "WHERE pmt_id = $pmt_id AND t.environment<>17 AND r.ticket_id is not null "
                                   "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                   "AND (d.name is null or d.name not like '%产品设计%') "
                                   + pmt_to_ibug_user_sql, vars=dev_value)[0]['count']

            major_bug_all = ibug_db.query(
                "SELECT t.status AS status,t.created_at AS created_at,"
                " t.id AS id,t.owner AS owner,t.created_at AS created_at,t.status AS status,MAX(l.created_at) AS verified_at "
                "FROM ticket AS t "
                "LEFT JOIN dd_common AS d "
                "ON t.reason = d.id "
                "LEFT JOIN ticket_log AS l "
                "ON t.id = l.ticket_id "
                "WHERE t.pmt_id =$pmt_id AND priority IN (6,7,8) "
                "AND (t.status !='closed' OR t.status ='closed' AND resolution NOT IN(20,27)) "
                "AND environment <>17 AND (d.name is null or d.name not like '%产品设计%')"+pmt_to_ibug_user_sql+"  GROUP BY id", vars=dev_value)
            major_bug = len(major_bug_all)
            repair_time = 0
            aday = 3600 * 24
            for item in major_bug_all:
                created = datetime_to_timestamp(item['created_at'])
                if item['status'] == 'closed':
                    end = datetime_to_timestamp(item['verified_at'])
                else:
                    end = int(time.time())
                repair_time += end - created
            repair_time = repair_time / aday

            test_to_dev = ibug_db.query("SELECT t.id,MAX(l.created_at) "
                                        "FROM ticket AS t "
                                        "LEFT JOIN dd_common AS d "
                                        "ON t.reason = d.id "
                                        "LEFT JOIN ticket_log AS l "
                                        "ON t.id = l.ticket_id "
                                        "WHERE  t.id = l.ticket_id "
                                        "AND pmt_id=$pmt_id AND environment = 16 "
                                        "AND (t.status !='closed' OR t.status ='closed' AND t.resolution NOT IN(20,27)) "
                                        "AND l.field='environment' AND l.oldvalue ='Test' AND l.newvalue='Dev' "
                                        "AND (d.name is null or d.name not like '%产品设计%') " + pmt_to_ibug_user_sql +
                                        "GROUP BY t.id", vars=dev_value)
            daily_to_rc = len(test_to_dev)
            rc = ibug_db.query("SELECT count(*) AS count "
                               "FROM ticket AS t "
                               "LEFT JOIN dd_common AS d "
                               "ON t.reason = d.id "
                               "WHERE  pmt_id=$pmt_id AND environment = 16 "
                               "AND (t.status !='closed' OR t.status ='closed' AND t.resolution NOT IN(20,27)) "
                               "AND (d.name is null or d.name not like '%产品设计%') " + pmt_to_ibug_user_sql,
                               vars=dev_value)[0]['count']

            puzzle_db.insert('rp_developer', staff_no=devs[i]['staff_no'], chinese_name=devs[i]['chinese_name'],
                             total=dev_count, workload=devs[i]['workload'] / 8, unclose=unclose, reject=reject,
                             reopen=reopen, repair_time=repair_time, major_bug=major_bug, daily_to_rc=daily_to_rc,
                             rc=rc, user_from=devs[i]['from'], pmtId=pmt_id)
        puzzle_db.delete('rp_qa', where='pmtId = $pmt_id', vars=value)
        error += "================qa start===============<br>"

        pmt_to_ibug_user_sql = ' AND chinese_name =$chinese_name '
        for i in qas:
            #user_name = qas[i]['email'].split('@')[0]+'@%'
            qa_value = {'pmt_id': pmt_id, 'chinese_name': qas[i]['chinese_name']}
            qa_count = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                                     "LEFT JOIN user AS u "
                                     "ON reporter = u.user_name "
                                     "WHERE pmt_id = $pmt_id "
                                     "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                     + pmt_to_ibug_user_sql, vars=qa_value)[0]['count']
            dailybuild = ibug_db.query("SELECT count(*) AS count FROM ticket AS t "
                                       "LEFT JOIN user as u "
                                       "ON reporter = u.user_name "
                                       "WHERE pmt_id = $pmt_id "
                                       "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                       "AND environment=17 " + pmt_to_ibug_user_sql, vars=qa_value)[0]['count']
            pre_priority = ibug_db.query("SELECT priority,c.name AS name ,count(*) AS count FROM ticket AS t"
                                         "LEFT JOIN user as u "
                                         "ON reporter = u.user_name "
                                         "LEFT JOIN dd_common as c "
                                         "ON priority = c.id "
                                         "WHERE pmt_id = $pmt_id "
                                         "AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27)) "
                                         "AND environment=18 " + pmt_to_ibug_user_sql +
                                         "GROUP BY priority", vars=qa_value)
            qa_priority = {'p1': 0, 'p2': 0, 'p3': 0, 'p4': 0}
            for priority in pre_priority:
                name = priority['name'].split('-')[0].lower()
                qa_priority[name] = priority['count']

            puzzle_db.insert('rp_qa', staff_no=qas[i]['staff_no'], chinese_name=qas[i]['chinese_name'],
                             total=qa_count, workload=qas[i]['workload'] / 8, p1=qa_priority['p1'],
                             p2=qa_priority['p2'], p3=qa_priority['p3'], p4=qa_priority['p4'],
                             dailybuild=dailybuild, user_from=qas[i]['from'], pmtId=pmt_id)
        rp_projectList = puzzle_db.select('rp_projectList', where='pmtId=$pmt_id', vars={'pmt_id': pmt_id})
        if len(rp_projectList) == 1:
            puzzle_db.update('rp_projectList', where='pmtId=$pmt_id', vars={'pmt_id': pmt_id},
                             last_updated=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        else:
            puzzle_db.insert('rp_projectList', pmtId=pmt_id)

        result = '统计信息更新成功'
    except Exception as err:
        result = pmt_id+'统计信息更新失败,错误信息：' +str(err)+error

        send_mail(pmt_id + '项目统计信息更新失败', '错误信息：' + str(err)+error)
    close_db(puzzle_db)
    close_db(ibug_db)
    close_db(puzzle_db)
    return result

def get_task_owners_from_pmt(pmt_db,pmt_id):


    dev = {}
    qa = {}
    owners = pmt_db.query("SELECT s.staff_no AS staff_no,s.email AS email, t.stage AS stage,SUM(t.workload) AS workload,s.chinese_name AS chinese_name "
                        "FROM task AS t,staff AS s "
                        "WHERE project_id = $pmt_id AND t.owner = s.id "
                        "AND ((stage=107 AND task_type_id IN (2,3))  OR (stage=108 AND task_type_id =4)) "
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




def get_ticket_person_liable_from_ibug(pmt_db,ibug_db,pmt_id):

    person_liable = {}
    value = {'pmt_id':pmt_id}
    sql = "SELECT DISTINCT person_liable FROM ticket \
        WHERE pmt_id = $pmt_id \
        AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27))"
    tickets = ibug_db.query(sql,value)
    for item in tickets:
        if item['person_liable']=='':
            continue
        person_tmp = item['person_liable'].split(';')
        if len(person_tmp) <1:
            continue
        person = person_tmp[0].split()
        value ={'chinese_name':person[0]}
        users = get_user_from_pmt(pmt_db,value)
        if len(users) > 0 :
            id = len(person_liable)
            person_liable[id] = {'workload':0,'from':2}
            user_tmp = users[0]
            for key in user_tmp:
                person_liable[id][key] = user_tmp[key]

    return person_liable




def get_ticket_reporters_from_ibug(pmt_db,ibug_db,pmt_id):


    reporters = {}
    reporters_tmp = ibug_db.query("SELECT distinct u.user_name,u.chinese_name AS chinese_name,u.email AS email FROM ticket AS t  \
            LEFT JOIN user AS u \
            ON t.reporter = u.user_name \
            WHERE pmt_id =$pmt_id  \
            AND (status <> 'closed' OR status ='closed' AND resolution NOT IN(20,27))",vars={'pmt_id':pmt_id})
    for reporter in reporters_tmp:
        #user = reporter['email'].split('@')[0]
        value ={'chinese_name':reporter['chinese_name']}
        tmp = get_user_from_pmt(pmt_db,value)
        if len(tmp) > 0:
            id = len(reporters)
            reporters[id] ={'workload':0,'from':2}
            user_tmp = tmp[0]
            for key in user_tmp:
                reporters[id][key] = user_tmp[key]

    return reporters

def get_user_from_pmt(pmt_db,value):
    tmp = pmt_db.query("SELECT staff_no,email,chinese_name \
            FROM staff \
            WHERE chinese_name=$chinese_name \
            ORDER BY id DESC ",vars=value)
    return tmp



def datetime_to_timestamp(dt):
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    #将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(str(dt), '%Y-%m-%d %H:%M:%S'))
    return int(s)

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

def close_db(db):
    connection = db.ctx['db']
    connection.close()
    return
