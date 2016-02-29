#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""


"""

import functools
import os
import sys

import cx_Oracle
import cymysql 

ORACLE_CONF = [

	{'db_flag':'db01' , 'user':'xxx' , 'passwd':'xxx','tns_names':'''(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xx)(PORT = 1522))) (CONNECT_DATA = (SID= xxxx)(SERVER = DEDICATED)))'''},

	{'db_flag':'db03' , 'user':'xxx' , 'passwd':'xxx','tns_names':'''(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = (PROTOCOL = TCP)(HOST = xxx.xxx.x.xx)(PORT = 1521)))(CONNECT_DATA =(SID = xxxx)))'''}

]

MYSQL_CONF = [

	{'db_flag':'db02','host':'xxx.xxx.xxx.xx','user':'xxxx','passwd':'xxxx','port':331x,'db':'xxx'},
	{'db_flag':'db04','host':'xxx.xxx.xxx.xx','user':'xxxx','passwd':'xxxx','port':331x,'db':'xxx'}
]

SQL_SELECT = [

	('db01',"select  vcwid, vcsvccode, vccustomer, inepid,vcareacode,ineid,vcsla,iworktype,iworkstatus,iworkresult,ifinishflag,isourceid,vcpara,icheckstatus,vccheckmask,dtctime from tneticket_adsl_history where rownum<5"),
#	('db01',"select TEMPLATE_ID,TEMPLATE_NAME,TEMPLATE_CODE,TEMPLATE_VAL,DSCOUNT,TEMPLATE_PRINT,ACTION_ID,STS,STS_DATE,REMARKS from print_template p where p.template_id='100099'"),
#	('db01',"select * from print_template p where p.template_id='100099'")

]

"""
(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35,:36,:37,:38,:39)
"""


SQL_INSERT = [

	('db02',"insert into tneticket_adsl values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"),
#	('db02',"insert into print_template  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"),
#	('db03',"insert into print_template  values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)")
]

