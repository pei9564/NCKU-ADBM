import pyodbc
import pandas as pd
import pymysql

is_equal = True
compare_table = '處分'


# 連接MS SQL

sql_server_driver = 'ODBC Driver 17 for SQL Server'
sql_server_server = 'LAPTOP-V7M8IDF4'
sql_server_database = 'AMDB'
sql_server_UID = 'sa'
sql_server_PWD = 'test1234'

connection_sql_server = pyodbc.connect(f'DRIVER={sql_server_driver};SERVER={sql_server_server};DATABASE={sql_server_database};UID={sql_server_UID};PWD={sql_server_PWD}')
cursor_sql_server = connection_sql_server.cursor()


# 連接 MariaDB

mariadb_host = '127.0.0.1'
mariadb_database = 'adbm'
mariadb_user = 'root'
mariadb_password = ''

connection_mariadb = pymysql.connect(host=mariadb_host, user=mariadb_database, password=mariadb_password, database=mariadb_database)
cursor_mariadb = connection_mariadb.cursor()


# 讀取 MS SQL 和 MariaDB 資料
cursor_sql_server.execute(f'SELECT * FROM {compare_table}') 
rows_sql_server = cursor_sql_server.fetchall()

cursor_mariadb.execute(f'SELECT * FROM {compare_table}') 
rows_mariadb = cursor_mariadb.fetchall()


# 關閉 cursor 和資料庫連接
connection_sql_server.close()
cursor_sql_server.close()

connection_mariadb.close()
cursor_mariadb.close()


# 逐一比較
for row_sql_server, row_mariadb in zip(rows_sql_server, rows_mariadb):

    tuple_rows_sql_server = tuple(row_sql_server)

    if tuple_rows_sql_server != row_mariadb:
        print(f'The tuple {tuple_rows_sql_server} is different in both databases.')
        IS_EQUAL = False

if is_equal:
    print(f'{compare_table} table 比對完成 !!!')
    