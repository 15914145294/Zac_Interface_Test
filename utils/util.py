# -*- coding: utf-8 -*-

import re
import datetime
import requests
from random import choice
from logs.logUtil import logger
from configs.ad09config import BASE_URL


class CommonMethods(object):
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

	@staticmethod
	def get_area_childs(AreaId):
		"""
		根据省份ID 获取城市明细
		:param AreaId:省份对应的AreaId 如广东
		:return: 返回随机一个城市 如 深圳
		"""
		data = {"AreaId":AreaId}
		r = requests.post(BASE_URL + "/service/getareachilds", data=data)
		childs = r.json()
		if childs:
			value = choice(childs)["Value"]
			return value
		else:
			return
	@staticmethod
    def get_city(AreaId):
        """获取城市列表"""
        d = dict()
        data = {"AreaId": AreaId}
        r = requests.post(BASE_URL + "/service/getareachilds", data=data)
        childs = r.json()
        """
        [{
	    'Key': '广州市',
	    'Value': 'c1795c20-32fb-4b67-ae76-c6aab6e24a43'
        }..
        """
        for i in childs:
            d[i["Key"]] = i["Value"]
        return d

    def parse_json(file):
        """
        解析json文件
        :param file: 文件路径
        :return: 包含json document的dict
        """
        try:
            fb = open(file, encoding="utf-8")
        except:
            raise ValueError("文件不存在")
        d = json.load(fp=fb)
        return d

if __name__ == '__main__':
	print(CommonMethods.get_area_childs("31b25d9c-912d-4db9-82ab-10d87a2885b3"))
