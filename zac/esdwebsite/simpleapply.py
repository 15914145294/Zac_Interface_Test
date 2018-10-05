# encoding:utf-8
import re
import json
import random
import string
from utils.singleton import singleton
from requests.sessions import Session
from configs.config import ConfigENum

@singleton
class Ad09Util(object):
	def __init__(self, url):
		"""
			请求http://uatweb.zac-esd.com/ad09
			设置content_type类型
			通过get_cookies获取ad09着陆页返回的cookies
			通过get_token获取着陆页返回的token
			通过make_mobile 随机生成144开头不含1442的手机号
		"""
		if not url:
			raise ValueError
		else:
			self.url = url
		self.s = Session()
		self.s.headers.setdefault("Content_type", "application/x-www-form-urlencoded")
		self.s.headers.update(Referer="%s/ad09" % ConfigENum.BASE_URL.value)
		# self.s.cookies.update(self.get_cookies()[0])
		self.result = self.get_cookies()
		self.req = self.result[1]

	def get_cookies(self):
		"""
		获取上一次请求的cookie
		:return: 返回cookie dict
		"""
		r = self.s.get(self.url)
		# print(r.cookies.get_dict())
		return (r.cookies, r.text)

	def get_token(self, req):
		pattern = 'name="__RequestVerificationToken" type="hidden" value="(.*)"'
		p = re.compile(pattern)
		if p.search(req):
			token = p.search(req).groups()[0]
			token = token.__str__().strip('"')
		else:
			return
		return token

	@staticmethod
	def get_mobile():
		s = "144"
		n = range(10)
		for i in range(8):
			s += random.choice(n).__str__()
			if len(s) == 4 and s == "1442":
				s = (int(s) - 1).__str__()
		return s

	@staticmethod
	def get_email():
		email_str = "{}@{}.com"
		suffix = ["gmail", "126", "yahoo", "hotmail", "sina", "sohu", "live", "163"]
		email = "".join(random.choice(string.ascii_letters) for x in range(8))
		email = email_str.format(email, random.choice(suffix))
		# print (email)
		return email

	@staticmethod
	def get_name():
		first_name_list = open(ConfigENum.FIRST_NAME.value, encoding='utf-8')  # 打开文件，获取文件句柄
		last_name_list = open(ConfigENum.LAST_NAME.value, encoding='utf-8')
		# 从文件中获取用load读取文件，并且把文件中的字符串转换成列表
		first_names = json.load(first_name_list)
		last_names = json.load(last_name_list)
		name_all = random.choice(last_names) + random.choice(first_names) + random.choice(first_names)
		return name_all

	@staticmethod
	def get_QQNumber():
		QQ = "".join(map(lambda x: random.choice(string.digits), range(8)))
		return QQ


if __name__ == '__main__':
	url = "%s/ad09" % ConfigENum.BASE_URL.value
	print(id(Ad09Util(url)))
	print(id(Ad09Util(url)))
