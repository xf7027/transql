#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""

Quick and dirty script to migrate tables from Oracle to MySQL

Information on using cx_Oracle can be found here:

http://www.oracle.com/technetwork/articles/dsl/prez-python-queries-101587.html

"""

import os,time
import sys
import cx_Oracle
import cymysql
import transql_conf 
from multiprocessing import Pool,freeze_support, set_start_method


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def get_table_metadata(cursor):
    table_metadata = []
    # "The description is a list of 7-item tuples where each tuple
    # consists of a column name, column type, display size, internal size,
    # precision, scale and whether null is possible."
    for column in cursor.description:
        table_metadata.append({
            'name' : column[0],
            'type' : column[1],
            'display_size' : column[2],
            'internal_size' : column[3],
            'precision' : column[4],
            'scale' : column[5],
            'nullable' : column[6],
        })
    return table_metadata


def create_table(mysql, table, table_metadata):
    sql = "CREATE TABLE %s (" % (table,)
    column_definitions = []

    for column in table_metadata:
        # 'LINES' is a MySQL reserved word
        column_name = column['name']
        if column_name == "LINES":
            column_name = "NUM_LINES"

        if column['type'] == cx_Oracle.NUMBER:
            column_type = "DECIMAL(%s, %s)" % (column['precision'], column['scale'])
        elif column['type'] == cx_Oracle.STRING:
            if column['internal_size'] > 256:
                column_type = "TEXT"
            else:
                column_type = "VARCHAR(%s)" % (column['internal_size'],)
        elif column['type'] == cx_Oracle.DATETIME:
            column_type = "DATETIME"
        elif column['type'] == cx_Oracle.FIXED_CHAR:
            column_type = "CHAR(%s)" % (column['internal_size'],)
        else:
            raise Exception("No mapping for column type %s" % (column['type'],))

        if column['nullable'] == 1:
            nullable = "null"
        else:
            nullable = "not null"

        column_definitions.append("%s %s %s" % (column_name, column_type, nullable))

    sql += ",".join(column_definitions)

    sql += ") DEFAULT CHARACTER SET = utf8;"

    print(sql)
    mysql.execute(sql)


def migrate_data(table):

    collection=transql_conf.create_collection()
    coll_oracle=collection[1]
    coll_mysql=collection[0]
    oracle_cursor=coll_oracle.cursor()
    oracle_cursor.execute("SELECT count(*) FROM %s" % (table,))
    mysql_cursor = coll_mysql
    total_rows = oracle_cursor.fetchone()[0]


    oracle_cursor.execute("SELECT * FROM %s" % (table,))

    table_metadata = get_table_metadata(oracle_cursor)

    create_table(coll_mysql, table, table_metadata)

    for x in range(total_rows):
       
	 # TODO: should probably use fetchmany() and transactions to speed things up
        row = oracle_cursor.fetchone()
        column_names=[]
        column_values=[]
        index = 0
        for column in table_metadata:
            if column['name'] == 'LINES':
                column_names.append('NUM_LINES')
            else:
                column_names.append(column['name'])
            column_values.append(row[index])
            index += 1
        question_marks = ",".join(["%s" for i in range(len(column_names))])
        sql_insert = "INSERT INTO %s (%s) VALUES (%s)" % \
                     (table, ",".join(column_names), question_marks)
        mysql_cursor.connection.commit()        
        mysql_cursor.execute(sql_insert, column_values)

def insert_data(list_s_i):
    info(list_s_i)
    collection=transql_conf.create_collection() 
    coll_oracle=collection[1]
    coll_mysql=collection[0]
    oracle_cursor = coll_oracle.cursor()
    oracle_cursor.execute(list_s_i[0])
    for row in oracle_cursor.fetchall():
        time.sleep(0.1)
        print(row)
        sql_select=[]
        sql_insert=[]
        sql_s_i=[]
        column_values = []
        index = 0
        line_count=len(row)
        for column in range(line_count):
            column_values.append(row[index])
            index += 1
        mysql_cursor = coll_mysql
        mysql_cursor.execute(list_s_i[1], column_values)
        mysql_cursor.connection.commit()

def pool_insert_data():

   
    sql_select=[]
    sql_insert=[]
    list_s_i=[]
    with open("./select.sql","r+") as file_select:
        for line in file_select:
            sql_select.append(line)
    with open("./insert.sql","r+") as file_insert:
        for line in file_insert:
            sql_insert.append(line)

    if len(sql_select)!=len(sql_insert):
        print ("select.sql lines not equal insert.sql lines")
    
    for a,b in zip(sql_select,sql_insert):
        list_s_i.append([a,b])
    PROCESSES=int(len(list_s_i))
    if PROCESSES>4 :
       PROCESSES=4
    with Pool(PROCESSES) as p:
        p.map(insert_data,list_s_i)


def migrate():
  try:
      tables = transql_conf.tables
  except AttributeError as e:
      print (e)
      sys.exit(1)             
  for table in tables:
      migrate_data(table)

if __name__=="__main__":

    if len(sys.argv) < 2:
        print ("""Usage: transql.py  <create|insert>

where CONFIG_MODULE is the name of a python module that defines 3 variables:
  oracle = a cx_Oracle connection object instance, to use for source
  mysql  = a MySQLdb connection object instance, to use for target
  tables = an iterable of string table names to migrate

Example:

# python transql.py create

""")
        sys.exit(0)

    freeze_support()
    set_start_method('spawn')

    action = sys.argv[1]

    if(action == 'create'):
             print ("create")
             migrate()
    else:
             print ("Insert")
             pool_insert_data()

	
