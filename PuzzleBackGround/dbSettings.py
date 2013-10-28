#encoding=utf8

import web
def getConnectionV2(name):
    db = {
        'puzzle': lambda: web.database(dbn='mysql',db='puzzle',user='root',pw='anjuke',host='192.168.190.59',port=3306),
        'pmt':lambda:  web.database(dbn='mysql',db='pmt_new',user='readonly_v2',pw='aNjuKe9dx1Pdw',host='10.10.8.14',port=3309),
        'ibug':lambda:  web.database(dbn='mysql',db='ibug_db',user='readonly_v2',pw='aNjuKe9dx1Pdw',host='10.10.8.14',port=3309),
        'ama':lambda:  web.database(dbn='mysql',db='Mobile',user='readonly_v2',pw='aNjuKe9dx1Pdw',host='10.10.8.14',port=3309),
    }[name]()
    return db

def close_db(db):
    connection = db.ctx['db']
    connection.close()
    pass
