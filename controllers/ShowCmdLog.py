#encoding=utf8

from config import settings
import web
import time

data = {'pageIndex':'project'}
render = settings.render
db = settings.db

class ShowCmdLog:
    def GET(self):
    # These headers make it work in browsers
        count = "100"
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')        
        yield '<h2>Prepare for Launch!</h2>'
        j = '<li>Liftoff in %s...<br>bblablablablablablablablablablablablablablablablablablablabla<br>blablablablablablablablablablablablablablablablablablablabl<br>ablablablablablablablablablablablablablablablablablab<br>lablablablablablablablablablablablablablablablablablablablablablablabl<br>ablablablablablablablablablablabl<br>ablablablablablablablablablablablablablablablablablablablablablablablabla<br>blablablablablablablablablablablablablablablablablablablablablablablablablabla<br>blablablablablablablablablablablablablablablablalablacasa</li>'
        yield '<ul>'
        count = int(count)

        for i in range(count,0,-1):
            out = j % i
            yield out
            yield '</ul><script type=\"text/javascript\">document.body.scrollTop = document.body.scrollHeight</script>'
            time.sleep(1)

        yield '<h1>Lift off</h1>'
