#encoding=utf8
import web


db = web.database(dbn='mysql',db='www',user='www',pw='www')
render = web.template.render('templates/',cache=False)

web.config.debug = True

config = web.storage(
		email = 'lenyemeng@anjukeinc.com',
		site_name = 'Puzzle -- iOS开发发布平台',
		site_desc = 'iOS开发发布平台',
		static = '/static',
		)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

allowed = (
		('test','test')
		)
