# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       Administrator
   date：          2018/8/18 0018
-------------------------------------------------
"""
import os
import yaml
from xlrd import open_workbook


class YamlReader(object):
	def __init__(self, yaml):
		"""
		如果yml配置文件存在就直接赋值
		如果不存在就抛出异常
		@yaml 配置文件的路径
		"""
		if os.path.exists(yaml):
			self.yaml = yaml
		else:
			raise FileNotFoundError("文件不存在")
		self._data = None

	@property
	def data(self):
		"""
		如果是第一次调用data，读取配置文件，否则直接返回之前保存的数据
		:return: 返回config配置的列表
		"""
		if not self._data:
			with open(self.yaml, "rb")as f:
				self._data = list(yaml.safe_load_all(f))
		return self._data


class ExcelReader(object):
	"""
		读取excel文件中的内容。返回list。

		如：
		excel中内容为：
		| A  | B  | C  |
		| A1 | B1 | C1 |
		| A2 | B2 | C2 |

		如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
		[{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

		如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
		[[A,B,C], [A1,B1,C1], [A2,B2,C2]]

		可以指定sheet，通过index或者name：
		ExcelReader(excel, sheet=2)
		ExcelReader(excel, sheet='BaiDuTest')
		"""

	def __init__(self, excel, sheet=0, title_line=True):
		if os.path.exists(excel):
			self.excel = excel
		else:
			raise FileNotFoundError("%s文件不存在" % excel)

		self.sheet = sheet
		self.title_line = title_line
		self._data = list()

	@property
	def data(self):
		if not self._data:
			workbook = open_workbook(self.excel)
			if type(self.sheet) not in [int, str]:
				raise Exception('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
			elif type(self.sheet) == int:
				s = workbook.sheet_by_index(self.sheet)
			else:
				s = workbook.sheet_by_name(self.sheet)

			if self.title_line:
				title = s.row_values(0)  # 首行为title
				for col in range(1, s.nrows):
					# 依次遍历其余行，与首行组成dict，拼到self._data中
					self._data.append(dict(zip(title, s.row_values(col))))
			else:
				for col in range(0, s.nrows):
					# 遍历所有行，拼到self._data中
					self._data.append(s.row_values(col))
			return self._data
