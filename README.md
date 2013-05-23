puzzle
======

iOS管理发布平台

###功能简述
鉴于目前iOS开发部门在开发过程中出现项目依赖的种种问题，以及项目在打daily build和RC package的时候出现很多失误，现在决定开发puzzle这个项目来解决当前遇到的问题，puzzle的主要功能点如下：

* 解决项目依赖，通过python脚本，处理在项目clone到本地、更新等操作的时候出现的依赖库版本未及时更新的窘境。
* 解决项目在发daily build和打渠道包的时候，出现的依赖库的版本不一致，从而导致测试遇到困扰的问题。

###参与开发人员
孟智	 田伟宇	丛贵明

###开发周期
5/20～6/20

###环境要求
* Python2.7
* web.py (`easy_install web.py`)
* MySQLdb (`easy_install MySQL-python`)
  Mako (`cd Mako-0.8.0 && python setup.py install`)
run `python server.py` 

###模块划分
