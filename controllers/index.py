#encoding=utf8
import web
import re
import base64

from config import settings

render = settings.render

class Index:
		''' 主页 '''
		def GET(self):
			return render.index("Hello World!")

		def POST(self):
			pass

class Login:
		def GET(self):
			auth = web.ctx.env.get('HTTP_AUTHORIZATION')
			authreq = False
			if auth is None:
				authreq = True
			else:
				auth = re.sub('^Basic','',auth)
				username,password = base64.decodestring(auth).split(':')
				if (username,password) in settings.allowed:
					raise web.seeother('/')
				else:
					authreq = True

			if authreq:
				web.header('WWW-Authenticate','Basic realm="Auth example"')
				web.ctx.status = '401 Unauthorized'
				return
