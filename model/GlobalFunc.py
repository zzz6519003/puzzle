#encoding=utf8
from config import common
import sys
import urllib

def get_pmt_url(pmt_id):
    return common.pmt_url+pmt_id
def get_ticket_url(ticket_id):
    return common.ticket_url+str(ticket_id)

def report_html(data,name,pmt_id,page,is_hyperlink,limit,is_color):
    color = ''
    bgcolor = ''
    s = ''
    if page in ('index','reason','component'):
        param = urllib.urlencode({'pmt_id':pmt_id,'page':page,'location':name})
        if page =='index':
            content = data[name]
        else:
            if name !='total':
                content = data['count']
            else:
                content = data
        if is_color ==1 and content < limit or is_color==2 and content > limit:
            color = 'red'
        s += '<span  style="background-color:'+bgcolor+';">'
        if is_hyperlink ==True:
            s+= '<a href="/report/detail?'+param+'" target="_blank"><font color="'+color+'">'+ str(content)+'</font></a>'
        else:
            s+= content
                                                                                                                                    
        s +='</span>'

        return s

    s = '<ul>'
    for i in data:
        #这些项不累加
        param = urllib.urlencode({'pmt_id':pmt_id,'cn_name':data[i]['chinese_name'],'page':page,'location':name})
        if name in ('p1','p2','p3','p4') and page =='qa':
            break
        if data[i]['chinese_name'] !='total':
            #来自ibug的开发或者测试变色
            if int(data[i]['user_from']) == 2 and name=='chinese_name':
                bgcolor = '#B0B85E'
            #超过限制的参数变色
            if is_color ==1 and data[i][name] < limit or is_color==2 and data[i][name]>limit:
                color = 'red'
            s += '<li><span  style="background-color:'+bgcolor+';">'
            if is_hyperlink ==True:
                s+= '<a href="/report/detail?'+param+'" target="_blank"><font color="'+color+'">'+str(data[i][name])+'</font></a>'
            else:
                s+= str(data[i][name])
            
            s +='</span></li>'
    if len(data) > 0:
        pos = len(data)-1
        param = urllib.urlencode({'pmt_id':pmt_id,'cn_name':data[pos]['chinese_name'],'page':page,'location':name})
        s += '<li><font color="'+color+'">'
        if is_hyperlink ==True :
            s += '<a href="/report/detail?'+param+'"target="_blank">'+str(data[pos][name])+'</a>'
        else:
            s += str(data[pos][name])
        s += '</font></li>'
    s += '</ul>'
    return s


    
