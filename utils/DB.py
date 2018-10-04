# encoding:utf-8


"""
@version: python27
@author: fafa
@site: http://www.phpgao.com
@software: PyCharm Community Edition
@file: mysql_db.py
@time: 2017/2/27 0027 下午 9:59
"""
import os
import mysql.connector
from configs.config import DB_NAME


# db_name = {'user': 'root', 'password': '123456', 'port': '3306', 'host': 'localhost', 'database': 'test'}



class MysqlDb(object):
	'''mysql db class'''

	def __init__(self, connect_db=DB_NAME):
		u'''初始化游标对象 数据库连接对象'''
		self.conect_db = connect_db
		self.con = None
		self.cur = None

	def get_cursor(self):
		self.con = mysql.connector.connect(**self.conect_db)
		if self.con:
			self.cur = self.con.cursor()

	def close_db(self):
		u'''关闭游标对象 提交事务 关闭数据库连接'''
		if self.cur:
			self.cur.close()
		if self.con:
			self.con.commit()
			self.con.close()

	def __enter__(self):
		self.get_cursor()
		return self.cur

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_val:
			print("Exception has generate", exc_val)
			print("mysql execute error")
		self.close_db()
