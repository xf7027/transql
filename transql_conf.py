
"""

Configuration file for migrating SDBM. No account names or passwords should be stored in this file.

"""

import getpass
import os
import sys

import cx_Oracle
import cymysql 


oracle = cx_Oracle.connect('user', 'password', "(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = 1.1.1.1)(PORT = 1521))) (CONNECT_DATA = (SID = sid)(SERVER = DEDICATED)))" )


mysql=cymysql.connect(host='1.1.1.2', user='test', passwd='test', port=8066,db='CPS')

tables = (
    'TABLE_NAME',
)
