puzzle
======

iOS管理发布平台

###功能简述
鉴于目前iOS开发部门在开发过程中出现项目依赖的种种问题，以及项目在打daily build和RC package的时候出现很多失误，现在决定开发puzzle这个项目来解决当前遇到的问题，puzzle的主要功能点如下：

* 解决项目依赖，通过python脚本，处理在项目clone到本地、更新等操作的时候出现的依赖库版本未及时更新的窘境。
* 解决项目在发daily build和打渠道包的时候，出现的依赖库的版本不一致，从而导致测试遇到困扰的问题。

###参与开发人员
孟智	 田伟宇 	丛贵明		钱玥婷

###开发周期
5/20～6/20

###环境要求
* Python2.7
* web.py (`easy_install web.py`)
* MySQLdb (`easy_install MySQL-python`)
  Mako (`cd Mako-0.8.0 && python setup.py install`)
run `python server.py` 

*mako文档地址: [Mako Document](http://docs.makotemplates.org/en/latest/)*

###开发规则
Controller里在头部请添加

	from config import settings
	data = {'pageIndex':'home'}
	render = settings.render

所有controller往view传递参数请一律使用，｀render.index(data=data)｀，data为字典类型，所有参数都封装在此字典内。

pageIndex为栏目名称，定义在base.html里，TODO：今后拿到config文件里去
	
	<%
    navData = [
    ["Home","/index"],
    ["DailyBuild","/dailyBuild"],
    ["RcBuild","/rcBuild"],
    ["AboutUs","/aboutUs"],
    ]
    %>


###模块划分

Home
======

主要功能：

* 常用链接 PMT/Blog/Wiki
* 平台介绍

Project
========
目前暂命名为DailyBuild

分为 index和detail两个主要页面

index：列表页，列出iOS目前的应用（Android的后续加入）

detail:项目核心页面，左侧是一个项目的TimeLine，记录项目的整个生命周期

	|
	| |---------|
	|-| BackLog |
	| |_________|
	|
	| |-------------------|
	|-| DailyBuild - 5/24 |
	| |___________________|
	|
	|
	.
	.
	.
	|
	|
	| |------------|
	|-|Release     |
	| |____________|
	|
	END

如图，这里面会记录该项目的关键结点，或者叫milestone（如何输入milestone，细节再讨论）

当鼠标点击这些关键结点的时候，可以触发相应时间，Event DashBoard在timeline右侧展现，*第一阶段我们先把dailybuild这个关键步骤搞定,请贵明准备好各个应用的daily build打包脚本*

关于我们
===========
移动团队风采建设
