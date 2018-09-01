# encoding:utf-8

import re
import json
import random
from esdapi.config import BASE_URL
from esdapi.esdutil import Ad09Util


class AccessApply(object):
	def __init__(self):
		"""
		初始化session 并设置header和cookie
		"""
		self.s = None
		self.obj = self.init_session()

	#
	# 产品Referer
	# /Apply/SelectProduct?accessId=ab9416a4-6139-4dde-9a85-520a4abed7b5&frompage=ZaEsd-Ad09-
	#
	# self.product_referer = BASE_URL + self.EntranceAssign()["location"]

	def init_session(self):
		"""
		初始化session，用于保持cookie
		:return: 返回Ad09Util类型的对象及session
		"""
		obj = Ad09Util("%s/ad09" % BASE_URL)
		self.s = obj.s
		self.s.headers.update(Referer="%s/ad09" % BASE_URL)
		self.s.cookies.update(obj.get_cookies()[0])
		# print(self.s.cookies,"*****")
		return (obj, self.s)

	def Ad09_index(self):
		obj = self.obj[0]
		# obj = Ad09Util("%s/ad09" % BASE_URL)
		# self.s = obj.s
		self.s.headers.update(Referer="%s/ad09" % BASE_URL)
		# self.s.cookies.update(obj.get_cookies()[0])
		param = {"__RequestVerificationToken": obj.get_token(),
		         "FromPage": "ZaEsd-Ad09-",
		         "FromSE": "",
		         "CustomerId": "",
		         "ProductType": "all",
		         "Amounts": 50000,
		         "LoanTerm": 24,
		         "Name": u"测试",
		         "Mobile": obj.make_mobile(),
		         "Province": "31b25d9c-912d-4db9-82ab-10d87a2885b3",
		         "City": "92ce2049-36bf-4ae6-b831-22359c38f337",
		         "hiddenLoanPurpose": 0,
		         "hiddenLoanPurposeDetail": "{8132707A-E2AE-4F58-85FC-F023277D845B}"}
		r = self.s.post(obj.url, data=param, allow_redirects=False)
		# print("Location url is:", r.headers["Location"])
		try:
			return (r.headers["Location"], json.loads(r.text))
		except:
			return (r.headers["Location"], r.text)

	def getareachilds(self):
		self.s = self.obj[1]
		r = self.s.post("%s/service/getareachilds" % BASE_URL, allow_redirects=False)
		try:
			return r.json()
		except:
			assert isinstance(r.text, str)
			return r.text

	def GetLoanPurposeChilds(self):
		self.s = self.obj[1]
		r = self.s.post("%s/service/GetLoanPurposeChilds" % BASE_URL, allow_redirects=False)
		try:
			return r.json()
		except:
			assert isinstance(r.text, str)
			return r.text

	def get_Estimate(self):
		# path = /ad09/Estimate?customerId=bb36179e-3687-4d2a-8fbc-fe69793d0375&frompage=ZaEsd-Ad09-'
		d = {}
		path = self.Ad09_index()[0]
		customer_id = path.__str__().split("&")[0].split("?")[1].split("=")[1]
		url = BASE_URL + path
		d["url"] = url
		self.s =self.obj[1]
		r = self.s.get(url)
		d["text"] = r.text
		d["customer_id"] = customer_id
		# print("The customer_id:", customer_id)
		return d

	def ad09_estimate(self):
		d = self.get_Estimate()
		url = "%s/ad09/Estimate" % BASE_URL
		obj = self.obj[0]
		self.s = self.obj[1]
		self.s.headers.update(Referer=d["url"])
		self.s.cookies.update(obj.get_cookies()[0])
		param = {
			"OccupationTypes": 0,
			"EntryYear": 2015,
			"EntryMonth": 1,
			"PayoffTypes": 0,
			"BankPayoff": 5000,
			"SheBao": 0,
			"HousingFund": 0,
			"BranchOtherInsurance": 3,
			"BranchHouseProperty": 0,
			"MortgageTime": 3,
			"FromPage": "ZaEsd-Ad09-",
			"CustomerId": d["customer_id"],
			"EstimateAreaType": 6,
			"ProductType": "all",
			"ChannelType": "PC",
			"__RequestVerificationToken": obj.get_token()
		}
		r = self.s.post(url, data=param, allow_redirects=False)

		try:
			return (json.loads(r.text))
		except:
			return (r.text)

	def EntranceAssign(self):
		"""
		申请入口，返回key包含Location,frompage,accessId，用于选择产品url
		:return:
		"""
		self.s = self.obj[1]
		location = self.Ad09_index()[0]
		# print (BASE_URL + location,"&&&&&")
		self.s.headers['Referer'] = BASE_URL + location
		result = self.ad09_estimate()
		path = None
		for key in dict(result).keys():
			if key.lower() == "url":
				path = result[key]
		url = BASE_URL + path
		# self.s = Ad09Util(url).s
		r = self.s.get(url, allow_redirects=False)
		location = r.headers["Location"]
		cookie = self.s.cookies.get_dict()
		# print(cookie, "**")
		assert "/Apply/SelectProduct" in r.text, "请求结果出错"
		# s =  /Apply/SelectProduct?accessId=ab9416a4-6139-4dde-9a85-520a4abed7b5&frompage=ZaEsd-Ad09-
		p = "^\/Apply.*(accessId)=(.*)\&(.*)=(.*)"
		d = {}
		try:
			m = re.compile(pattern=p).search(location).groups()
			if m:
				d[str(m[0]).lower()] = m[1]
				d[str(m[2]).lower()] = m[3]
				d["location"] = location
				d["cookie"] = cookie
				return d

			else:
				return location
		except:
			return r.text

	def SelectProduct(self):
		"""
		返回选择产品界面，以供customparser解析符合的产品列表
		:return:
		"""
		# print(self.s.cookies,"******")
		url = BASE_URL + self.EntranceAssign()["location"]
		self.s = Ad09Util(url).s
		r = self.s.get(url, allow_redirects=False)
		return (r.cookies, r.text)

#
if __name__ == '__main__':
	print(AccessApply().SelectProduct())