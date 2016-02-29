1 版本说明（文档适用范围说明）  
  
操作系统：CentOS 6+ Minimal、SELinux disabled、Firewall disabled  
软件版本：0.0.8   
依赖软件及版本：gcc，python3.x，cx_Oracle-5.1.2，cymysql-0.8.5  
  
2 简介  
Oracle和Mysql互相迁移数据，可同时迁移多个不同数据库数据（并发的将数据在oracle和mysql之间随意迁移），效率高（实际测试表明，将100万数据从oracle迁移到mysql耗时2分30秒，其中1分30秒耗在oracle查询上），支持LOB字段迁移，支持中文数据迁移。  
  
3 部署  
3.1 基本安装  
3.1.1 安装python3.x  
$ ./rpm –ivh python-3.x-64.el6.x86_64.rpm  
3.1.2 安装oracle数据库模块  
3.1.2.1 安装oracle简易客户端  
解压basic-10.2.0.5.0-linux-x64.zip，将解压出来的instantclient_10_2上传至服务器 /mysql/component  
--版本号最好和在用的oracle数据库版本保持一致。  
3.1.2.2 设置环境变量  
$ cd ~  进入用户目录  
$ vi .bash_profile  添加如下行  
export ORACLE_HOME=/mysql/component/instantclient_12_1  
export TNS_ADMIN=/mysql/component/instantclient_12_1  
export NLS_LANG='SIMPLIFIED CHINESE_CHINA.ZHS16GBK'  
export NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS'  
$ source .bash_profile 使新增的变量生效  
3.1.2.3 导入ORA文件  
将TNSNAMES.ORA放入 /mysql/component/instantclient_10_2目录内  
3.1.2.4 安装oracle模块  
$ rpm –ivh cx_Oracle-5.1.2-10g-py26-1.x86_64.rpm  
3.1.3 安装mysql数据库模块  
3.1.3.1 安装mysql类包  
$ rpm –ivh mysql-libs-5.1.73-5.el6_6.x86_64  
3.1.3.2 安装cymysql模块  
$ tar xzvf cymysql-0.8.5.tar.gz  
$ cd cymysql-0.8.5  
$ python setup.py build  
$ python setup.py install  
  
4 运维  
4.1 日常操作  
4.1.1 配置数据源  
编辑transql_conf.py，将oracle和mysql的连接配置分别放在ORACLE_CONF和MYSQL_CONF列表里  
$ vi transql_conf.py   

ORACLE_CONF = [   

	{'db_flag':'db01' , 'user':'xxx' , 'passwd':'xxx','tns_names':'''(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xx)(PORT = 1522))) (CONNECT_DATA = (SID= xxxx)(SERVER = DEDICATED)))'''},

	{'db_flag':'db03' , 'user':'xxx' , 'passwd':'xxx','tns_names':'''(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xx)(PORT = 1521)))(CONNECT_DATA =(SID = xxxx)))'''}   
]

MYSQL_CONF = [   
	
	{'db_flag':'db02','host':'xxx.xxx.xxx.xx','user':'xxxx','passwd':'xxxx','port':331x,'db':'xxx'},
	
	{'db_flag':'db04','host':'xxx.xxx.xxx.xx','user':'xxxx','passwd':'xxxx','port':331x,'db':'xxx'}    
]

  
4.1.2 配置查询和插入语句
将提取数据的语句放在SQL_SELECT列表里，插入数据的语句放在SQL_INSERT列表里。db01,db02,db03,db04为4.1.1配置的db_flag标识，要注意SQL_INSERT列表里oracle和mysql的占位符不同，mysql是“%s”，oracle是“:“加数字。如果查询的表里有LOB字段，且是从oracle迁移到mysql，应单独执行迁移数据。

SQL_SELECT = [
	('db01',"select  vcwid, vcsvccode, vccustomer, inepid,vcareacode,ineid,vcsla,iworktype,iworkstatus,iworkresult,ifinishflag,isourceid,vcpara,icheckstatus,vccheckmask,dtctime from tneticket_adsl_history where rownum<5"),
	('db04',"select * from print_template p where p.template_id='100099'")
]

SQL_INSERT = [
	('db02',"insert into tneticket_adsl values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"),
	('db03',"insert into print_template  values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)")
]  

   
4.1.3 执行脚本 
执行脚本  
$ python transql.py   
如果查询的数据里有LOB，后面加“y“：   
$ python transql.py y   
目前测试发现：mysql至mysql，mysql至oracle，oracle至oracle间迁移LOB数据不需要特殊处理（即不需要加y）。   

5 新版本特征   
5.1 移除
去掉了原先版本中失败率极高的表创建功能，以后会专门写个程序实现此功能；
去掉了insert和select两个配置文件。    
5.2 新增
增加了oracle至oracle，mysql至mysql，mysql至oracle迁移功能；    
增加了LOB字段迁移功能；   
增加了数据分片插入功能，配合插入多进程大大提高了数据迁移速度；    
增加了一些显示运行状态的日志。    
5.3 更改
更改了程序结构，程序代码较原先版本变得清晰。
