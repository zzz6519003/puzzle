#encoding=utf8

import web
from web.contrib.template import render_mako
from settingsPersonality import getConnection


render = render_mako(
                    directories = ['templates'],
                    input_encoding='utf8',
                    output_encoding='utf8',
                    )
web.config.debug = True

config = web.storage(
        email = 'lenyemeng@anjukeinc.com',
        site_name = 'Puzzle -- iOS开发发布平台',
        site_desc = 'iOS开发发布平台',
        static = '/static',
        )

#db = web.database(dbn='mysql',db='puzzle',user='root',pw='casacasa',host='localhost',port=3306);
db = getConnection()

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
web.template.Template.globals['pageIndex'] = "index"

allowed = (
        ('test','test')
        )

