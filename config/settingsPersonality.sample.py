#encoding=utf8

import web

def getConnection():
    '''get connection of database'''
    db = web.database(dbn='mysql',db='puzzle',user='root',pw='casacasa',host='localhost',port=3306);
    return db
