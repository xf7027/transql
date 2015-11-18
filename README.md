1 本程序修改自 https://github.com/codeforkjeff/oracle2mysql

2 版本说明（文档适用范围说明）

操作系统：CentOS 7 Minimal、SELinux disabled、Firewall enable
软件版本：0.0.2
依赖软件及版本：gcc，python2.6，cx_Oracle-5.1.2，cymysql-0.8.5

3 简介
从oracle迁移表到mysql时，先提取oracle表的元数据，转换成mysql对应的数据并生成一个同名的表，然后将数据一行一行导入mysql。
从oracle查找数据插入到mysql时，需要提前在mysql建好对应的表，且表的列属性不能和oracle表查出的列属性有根本性的区别，程序会一次读入所有查找的数据，然后循环插入mysql对应的表。

4 部署
4.2 基本安装
4.2.1 安装python2.6
$ ./rpm –ivh python-2.6.6-64.el6.x86_64.rpm
4.2.2 安装oracle数据库模块
4.2.2.1 安装oracle简易客户端
解压basic-10.2.0.5.0-linux-x64.zip，将解压出来的instantclient_10_2上传至服务器 /mysql/component
--版本号最好和在用的oracle数据库版本保持一致。
4.2.2.2 设置环境变量
$ cd ~  进入用户目录
$ vi .bash_profile  添加如下行
export ORACLE_HOME=/mysql/component/instantclient_12_1
export TNS_ADMIN=/mysql/component/instantclient_12_1
export NLS_LANG='SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
export NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS'
$ source .bash_profile 使新增的变量生效
4.2.2.3 导入ORA文件
将TNSNAMES.ORA放入 /mysql/component/instantclient_10_2目录内
4.2.2.4 安装oracle模块
$ rpm –ivh cx_Oracle-5.1.2-10g-py26-1.x86_64.rpm
4.2.3 安装mysql数据库模块
4.2.3.1 安装mysql类包
$ rpm –ivh mysql-libs-5.1.73-5.el6_6.x86_64
4.2.3.2 安装cymysql模块
$ tar xzvf cymysql-0.8.5.tar.gz
$ cd cymysql-0.8.5
$ python setup.py build
$ python setup.py install

5 运维
5.1 日常操作
5.1.1 从oracle完全拷贝一个表到mysql
编辑transql_conf.py，在tables添加要拷贝的表名
$ vi transql_conf.py 
tables = (
    'work_area',
)
配置oracle连接串
oracle = cx_Oracle.connect('user', 'passwd', "(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = host_ip)(PORT = 1522))) (CONNECT_DATA = (SID = sxzy01)(SERVER = DEDICATED)))" )
--根据TNSNAMES.ORA文件配置，不一定和上面例子完全一样

配置mysql连接串
mysql=cymysql.connect(host='host_ip', user='test', passwd='test', port=8066,db='CPS')
--按实际情况填写, CPS为表所在的数据库名

执行脚本
$ python transql.py transql_conf.py create 
5.1.2 从oracle查找部分数据插入到mysql
编辑select.sql，写入查找语句，例：
select work_area_id,name,work_type_id,area_id,work_mode from work_area 
--也可以多表关联查询

编辑insert.sql，写入插入语句，例：
insert into work_area (work_area_id,name,work_type_id,area_id,work_mode) values (%s,%s,%s,%s,%s)
--表必须在mysql已存在，且字列属性应该和oracle上对应的列属性差别
执行脚本
$ python transql.py transql_conf.py insert
