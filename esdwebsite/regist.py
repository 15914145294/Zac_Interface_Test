# encoding:utf-8

import re
import json
import random
from requests.sessions import Session


class Regist(object):
	def __init__(self):
		"""
		初始化session 并设置header和cookie
		"""
		self.url = "http://uatweb.zac-esd.com/Account/Regist"
		self.s = Session()
		self.s.headers.setdefault("Content_type", "application/x-www-form-urlencoded")
		self.s.cookies.update(self.get_cookies()[0])

	# self.s.headers.update({"Cookies": self.get_cookies()})

	def get_cookies(self):
		"""
		获取上一次请求的cookie
		:return: 返回cookie dict
		"""
		r = self.s.get(self.url)
		print(r.cookies.get_dict())
		return (r.cookies.get_dict(), r.text)

	def get_token(self):
		"""
		获取上一次请求隐匿的表单token
		:return:
		"""
		pattern = 'name="__RequestVerificationToken" type="hidden" value="(.*)"'
		p = re.compile(pattern)
		text = self.get_cookies()[1]
		if p.search(text):
			token = p.search(text).groups()[0]
			token = token.__str__().strip('"')
		else:
			return
		return token

	def get_mobile(self):
		s = "144"
		n = range(10)
		for i in range(8):
			s += random.choice(n).__str__()
			if len(s) == 4 and s == "1442":
				s = (int(s) - 1).__str__()
		print(s)
		return s

	def regist(self):
		param = {"__RequestVerificationToken": self.get_token(),
				 "MobilePhone": self.get_mobile(),
				 "PassWord": "123456a",
				 "ConfirmPassword": "123456a",
				 "IntroducerMobile": "",
				 "IsAcceptPact": "true"}
		r = self.s.post(self.url, data=param)
		try:
			return json.loads(r.text)
		except:
			return r.text


if __name__ == '__main__':
	print(Regist().regist())
