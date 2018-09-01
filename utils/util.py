# -*- coding: utf-8 -*-

import re
import datetime
from logs.logUtil import logger


class UtilMethod(object):
	@staticmethod
	def read_file(file_path="", encoding="utf-8"):
		"""
		读取一个文件
		:param file_path: 路径
		:param encoding: 编码
		:return: 文件中的内容
		"""
		try:
			with open(file_path, 'r', encoding=encoding) as f:
				return f.read()
		except BaseException as e:
			print("Error: %s " % e)

	@staticmethod
	def get_time():
		"""
		获取一个时间点
		:return: 返回时间点
		"""
		return datetime.datetime.now().strftime('%Y-%m-%path_dict-%H-%M-%S')

	@staticmethod
	def case_argument_print(data):
		"""
		case信息输出
		"""
		print("|---请求详情:")
		logger.info("|---请求详情:")
		for k, v in data.items():
			print("|------%s:%s" % (k, v))
			logger.info("|------%s:%s" % (k, v))

	@staticmethod
	def search_regular_data(data, pattern):
		"""
		通过正则表达式匹配数据 返回匹配的结果
		:param data: 需要匹配的数据
		:param pattern: 正则表达式
		:return:
		"""
		r = re.compile(pattern)
		if r.search(data):
			m = r.search(data).groups()
			if len(m) < 3:
				return m[0]
			else:
				return m
		else:
			raise ValueError("The pattern not matched data")

			# if __name__ == '__main__':
			# 	s = "/SalaryApply2?accessId=64ba0030-98ce-4db3-b5af-52cf111ad189&assignId=c4063653-a3cf-4632-9681-b6b37321922a&selectProductCode=Select_Product_Program_Web_Y&fromPage=ZaEsd-Ad09"
			# 	p = r".*assignId=(.*)&selectProductCode.*"
			# 	print(UtilMethod.search_regular_data(s,p))
