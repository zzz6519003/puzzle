#encoding=utf8

import web
from web.contrib.template import render_mako
from settingsPersonality import getConnection, changeDirect
from settingsReport import getConnectionV2
import os

changeDirect()

render = render_mako(
                    directories = ['templates'],
                    input_encoding='utf8',
                    output_encoding='utf8',
                    )
web.config.debug = True
web.config.cache = False

config = web.storage(
        email = 'lenyemeng@anjukeinc.com',
        site_name = 'Puzzle -- 移动开发发布平台',
        site_desc = '安居客移动开发发布平台',
        static = '/static',
        )

#db = web.database(dbn='mysql',db='puzzle',user='root',pw='casacasa',host='localhost',port=3306);
#db = getConnection()
#puzzle_db = getConnection()
#pmt_db = getConnectionV2('pmt')
#ibug_db = getConnectionV2('ibug')
#ama_db = getConnectionV2('ama')


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
web.template.Template.globals['pageIndex'] = "index"

allowed = (
        ('test','test')
        )

