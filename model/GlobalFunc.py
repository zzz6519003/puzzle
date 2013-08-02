#encoding=utf8
from config import common
import sys

def get_pmt_url(pmt_id):
    return common.pmt_url+pmt_id

def report_html(data,name,pmt_id,type,is_hyperlink,limit,is_color):
    s = '<ul>'
    color = ''
    bgcolor = ''
    for i in data:
        #这些项不累加
        if name in ('p1','p2','p3','p4') and type =='qa':
            break
        if data[i]['chinese_name'] !='total':
            #来自ibug的开发或者测试变色
            if int(data[i]['user_from']) == 2 and name=='chinese_name':
                bgcolor = '#B0B85E'
            #超过限制的参数变色
            if is_color ==1 and data[i][name] < limit or is_color==2 and data[i][name]>limit:
                color = 'red'
            s += '<li><span  style="background-color:'+bgcolor+';"><font color="'+color+'">'+str(data[i][name])+'</font></span></li>'
    if len(data) > 0:
        s += '<li><font color="'+color+'">'+str(data[len(data)-1][name])+'</font></li>'
    s += '</ul>'
    return s

    
