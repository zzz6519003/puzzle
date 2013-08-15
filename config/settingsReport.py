#encoding=utf8

import web

def getConnection():
    '''get connection of database'''
    db = web.database(dbn='mysql',db='puzzle',user='root',pw='casacasa',host='localhost',port=3306);
    return db

def getConnectionV2(name):
    db = {
        'puzzle': lambda: web.database(dbn='mysql',db='puzzle',user='root',pw='password',host='192.168.1.194',port=3306),
        'pmt':lambda:  web.database(dbn='mysql',db='pmt_new',user='readonly_v2',pw='aNjuKe9dx1Pdw',host='10.10.8.7',port=3309),
        'ibug':lambda:  web.database(dbn='mysql',db='ibug_db',user='readonly_v2',pw='aNjuKe9dx1Pdw',host='10.10.8.7',port=3309),
        }[name]()

    return db
