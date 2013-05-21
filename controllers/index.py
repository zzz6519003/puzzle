#encoding=utf8


from config import settings

render = settings.render

class Index:
		''' 主页 '''
		def GET(self):
			return render.index("Hello World!")

		def POST(self):
			pass


