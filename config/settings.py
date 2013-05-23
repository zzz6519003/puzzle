#encoding=utf8

import web
import settingsPersonality
from web.contrib.template import  render_mako


render = render_mako(
					directories = ['templates'],
					input_encoding='utf-8',
					output_encoding='utf-8',
					)
web.config.debug = True

config = web.storage(
		email = 'lenyemeng@anjukeinc.com',
		site_name = 'Puzzle -- iOS开发发布平台',
		site_desc = 'iOS开发发布平台',
		static = '/static',
		)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
web.template.Template.globals['pageIndex'] = "index"

allowed = (
		('test','test')
		)


