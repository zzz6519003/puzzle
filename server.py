#!/usr/bin/python
from config.url import urls
import web

app = web.application(urls,globals())

if __name__ == "__main__":
	app.run()
