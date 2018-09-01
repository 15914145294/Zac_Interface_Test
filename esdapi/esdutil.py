# encoding:utf-8
import re
import random
import string
from esdapi.config import BASE_URL
from requests.sessions import Session


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

	def get_cookies(self):
		"""
		获取上一次请求的cookie
		:return: 返回cookie dict
		"""
		r = self.s.get(self.url)
		# print(r.cookies.get_dict())
		return (r.cookies, r.text)

	def get_token(self):
		pattern = 'name="__RequestVerificationToken" type="hidden" value="(.*)"'
		p = re.compile(pattern)
		text = self.get_cookies()[1]
		if p.search(text):
			token = p.search(text).groups()[0]
			token = token.__str__().strip('"')
		else:
			return
		return token

	def make_mobile(self):
		s = "144"
		n = range(10)
		for i in range(8):
			s += random.choice(n).__str__()
			if len(s) == 4 and s == "1442":
				s = (int(s) - 1).__str__()
		return s

	def get_email(self):
		email_str = "{}@{}.com"
		suffix = ["gmail", "126", "yahoo", "hotmail", "sina", "sohu", "live", "163"]
		email = "".join(random.choice(string.ascii_letters) for x in range(8))
		email = email_str.format(email, random.choice(suffix))
		# print (email)
		return email

#
# if __name__ == '__main__':
# 	url = "%s/ad09" % BASE_URL
# 	Ad09Util(url).get_cookies()
# 	print(Ad09Util(url).get_email())
