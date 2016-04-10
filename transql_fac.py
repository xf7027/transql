#!/usr/bin/python
# -*- coding: UTF-8 -*-



import functools
import os
import sys
from time import sleep
import cx_Oracle
import cymysql 

import transql_conf


def exc(func):
	@functools.wraps(func)
	def wrapper(*args,**kw):
		try:
			return func(*args,**kw)
		except Exception as e:
			print("call",func.__name__,"error!!!  err_message: ",e)
			sys.exit(1)
	return wrapper


class Db_sql(object):

	def __init__(self,sql,value = None):
		self.sql = sql
		self.value = value

	def isemptyvalue(self):
		if(self.value == None):
			return 1
		else:
			return 0


class Db_obj(object):
	
	def __init__(self,lob_flag):
		print("init Db_obj ",__name__)
		self.conn = None
		self.cursor = None
		self.lob_flag = lob_flag

	@exc
	def get_result(self,db_sql):
		print("start execute ",db_sql.sql)
		rows=self.cursor.execute(db_sql.sql)
		if(self.lob_flag in ('y','Y')):
			return self.LOB_format(self.cursor)
		elif(self.lob_flag in ('n','N')):
			return list(self.cursor)
		else:
			print("LOB_FLAG not valid arguments")
			sys.exit(1)

	@exc
	def get_result_many(self,db_sql):
		if(db_sql.isemptyvalue()):
			row_num = self.cursor.executemany(db_sql.sql,[])
		else:
		#	print("start execute ","sql:",db_sql.sql,"value:",db_sql.value)
			print("===========",len(db_sql.value))
			row_num = self.cursor.executemany(db_sql.sql,db_sql.value)
		print(__name__,"execute",row_num,"lines")
		self.conn.commit()

	def wrap_sql_execute_values(self,db_sql):
		def sql_execute_values(value):
			self.cursor.execute(db_sql.sql,value)
			self.conn.commit()
			return 0
		return sql_execute_values

	def LOB_format(self,cursor):
		print("start LOB_format")
		row_value_b = []
		row_value=cursor.fetchone()
		while(row_value!=None): 
			col_value = []
			for col in row_value:
				if(type(col) == cx_Oracle.LOB):
					col = col.read()
					col = col.decode(encoding='gbk', errors='ignore')
					col_value.append(col)
				else:
					col_value.append(col)
		#		print("col_value:",type(col_value),col_value,"\n")
			row_value_b.append(col_value)
			row_value=cursor.fetchone()
		return row_value_b


class Db_obj_oracle(Db_obj):
	@exc
	def create_conn(self,kw):
		os.environ['NLS_LANG']='AMERICAN_AMERICA.zhs16gbk'
		with cx_Oracle.connect(kw['user'], kw['passwd'], kw['tns_names']) as oracle:
			self.conn = oracle
			self.cursor = oracle.cursor()
			print(self.cursor)

class Db_obj_mysql(Db_obj):
	@exc	
	def create_conn(self,kw):
		with cymysql.connect(host=kw['host'], user=kw['user'], passwd=kw['passwd'], port=kw['port'],db=kw['db']) as mysql:
			self.conn = mysql.connection
			self.cursor = mysql


@exc	
def create_db_obj(db_flag,lob_flag = 'N'):
	print(lob_flag)
	for v_dict in transql_conf.ORACLE_CONF:
		if(v_dict['db_flag'] == db_flag):
			ins_db_obj = Db_obj_oracle(lob_flag = lob_flag)
			ins_db_obj.create_conn(v_dict)
	for v_dict in transql_conf.MYSQL_CONF:
		if(v_dict['db_flag'] == db_flag):
			ins_db_obj = Db_obj_mysql(lob_flag = lob_flag)
			ins_db_obj.create_conn(v_dict)
	return ins_db_obj
