#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import os,time,sys
import cx_Oracle
import cymysql
import ctypes 
import transql_conf 
from transql_fac import exc,create_db_obj,Db_sql
import multiprocessing
import multiprocessing.pool
from multiprocessing import Pool,freeze_support, set_start_method

def info(title):
	print("----------------------------------------------------")
	print(title)
	print('module name:', __name__)
	print('parent process:', os.getppid())
	print('process id:', os.getpid())


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
	def _get_daemon(self):
		return False
	def _set_daemon(self, value):
		pass
	daemon = property(_get_daemon, _set_daemon)


class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


@exc
def l_slice(list):
	print("start l_slice")
	length = len(list)
	block_size = 50000
	rem = length%block_size
	if rem>0:
		rem = 1
	num = length // block_size + rem
	
	tem = 0
	r_list = [] 
	while(num):
		r_list.append(list[tem:tem+block_size])
		tem = tem + block_size
		num = num - 1
	print("end l_slice")
	return r_list


@exc
def insert_sql_execute(args):
	d_db_flag = args[0]
	ins_db_obj = create_db_obj(d_db_flag,'N')
	ins_sql = Db_sql(args[1],args[2:])		
#	sql_execute = ins_db_obj.wrap_sql_execute_values(ins_sql)
#	list(map(sql_execute,ins_sql.value))	
	ins_db_obj.get_result_many(ins_sql)
	return 0


def select_sql_execute(args):
	s_db_flag = args[0]
	d_db_flag = args[2]	
	s_sql = args[1]
	d_sql = args[3]


	print("from ",s_db_flag,"to ",d_db_flag)
	print("select sql:",s_sql)
	print("insert sql:",d_sql)
	
#	so = ctypes.CDLL("./getlobflag.so")


#	LOB_FLAG = chr(so.getlobflag())
	ins_db_obj = create_db_obj(s_db_flag,LOB_FLAG)
	print(ins_db_obj)
	ins_sql = Db_sql(s_sql)
	l_values = ins_db_obj.get_result(ins_sql)
	
	l_insert_conf = [d_db_flag,d_sql]
	l_insert = list(map(lambda l:l_insert_conf+l,l_slice(l_values)))	

	with Pool(len(l_insert)) as p:
		p.map(insert_sql_execute,l_insert)
	return 0


@exc
def pool_init():

	p_sql_select = transql_conf.SQL_SELECT
	p_sql_insert = transql_conf.SQL_INSERT
	p_sql_s_i = []	

	for a,b in zip(p_sql_select,p_sql_insert):
		p_sql_s_i.append(a+b)

#	C_FLAG = input("continue?  Y/y: ")
#	if C_FLAG not in ('y','Y'):
#		sys.exit(0)

	freeze_support()
	set_start_method('fork')
	with MyPool(4) as p:
		result = p.map(select_sql_execute,p_sql_s_i)
	print("call pool_init() result: ",result)
	return 0

if __name__ == "__main__":

	if len(sys.argv) == 2 and (sys.argv[1] in ['Y','y']):
		LOB_FLAG = 'Y'	
	elif len(sys.argv) == 1:
		LOB_FLAG = 'N'
	else:
		print("arg numbers error!")
		sys.exit(1)
	pool_init()
