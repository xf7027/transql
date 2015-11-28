#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""

Configuration file for migrating SDBM. No account names or passwords should be stored in this file.

"""

import getpass
import os
import sys

import cx_Oracle
import cymysql 

def create_collection():
  collect=[]
  os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
  with cymysql.connect(host='xx.xx.xx.xx', user='test', passwd='test', port=8066,db='xx') as mysql:
      collect.append(mysql)
  with cx_Oracle.connect('username', 'userpasswd', "(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = xx.xx.xx.xx)(PORT = xx))) (CONNECT_DATA = (SID= xx)(SERVER = DEDICATED)))" ) as oracle:
      collect.append(oracle)
  return collect
tables = (
    'work_area',
)

