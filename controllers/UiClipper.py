#encoding=utf8
from config import settings
from web import form
render = settings.render
db = settings.db
data = {'pageIndex':'uicomponent'}


class Index:
    
    def GET(self):
        #获取当前日期
        import time
        data['currentDate'] = time.strftime('%Y-%m-%d,%A',time.localtime(time.time()));
        
        #获取项目列表
        data['projectList'] = db.select('projectList', order="id ASC", _test=False);
        temp = [];
        for item in data['projectList']:
            item['lastUpdate'] = time.strftime('%Y-%m-%d,%H:%M',time.localtime(item['lastUpdate']));
            temp.append(item);
        data['projectList'] = temp;
        #获取数据
        return render.projectList(data=data);
    
addForm = form.Form(
        form.Textbox('ClipName', class_='clipName', description='ClipName: ', placeholder='please input the clip name'),
        form.Dropdown('Category', [(1,'iOS'), (2,'android')], class_='category', description='Category:'),
        );
            
class clipAdd:
    def GET(self):
        #展示添加页面
        f = addForm();
        data['form'] = f;
        return render.uiCliperAdd(data=data);
    
class addPicture:
    def GET(self):
        return ;
    
    def POST(self):
        return ;
        
class mobileUi:
    def GET(self):
        return render.mobileUi(data=data);
        
        
        
