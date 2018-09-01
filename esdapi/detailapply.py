# encoding:utf-8

from esdapi.access import AccessApply
import collections
from esdapi.config import BASE_URL
from esdapi.costomparser import get_products
from esdapi.esdutil import Ad09Util

access = AccessApply()
referer = BASE_URL + access.EntranceAssign()["location"]


class DetailApply(Ad09Util):
	def __init__(self, url):
		Ad09Util.__init__(self, url=url)
		self.d = collections.OrderedDict()
		self.a = access
		self.s = access.obj[1]
		self.get_access_id()

	def get_access_id(self):
		d = self.a.EntranceAssign()
		if isinstance(d, dict):
			self.d['accessID'] = d["accessid"]
			self.d['fromPage'] = d["frompage"]
		return True

	@property
	def match_products(self):
		html = self.a.SelectProduct()[1]
		MATCHED_PRODUICT = get_products(html)
		if MATCHED_PRODUICT:
			return MATCHED_PRODUICT
		else:
			return None

	def confirm_product(self, product="salary"):
		"""
		产品确认
		:return: 返回Location，详细申请第一步
		"""
		self.get_access_id()
		p = {"productType": "salary"}
		# self.d.update(productType="salary")
		param = {**self.d, **p}
		assert product in self.match_products, "The product not matched"

		url = BASE_URL + "/Apply/ComfirmProduct"
		self.s.headers["Referer"] = referer
		r = self.s.get(url, params=param, allow_redirects=False)
		# print(self.s.cookies, 0)
		return r.headers["Location"]

	def SelectChannel(self):
		"""
		选择产品渠道，线上，线下
		:return:
		"""
		path = self.confirm_product()
		url = BASE_URL + path
		# self.s.headers["Referer"]=
		r = self.s.get(url, allow_redirects=False)
		# print(self.s.cookies, 1)
		try:
			return (url, r.text)
		except:
			return (r.text)

	def ComfirmChannel(self):
		"""
		确认渠道
		:return:
		"""
		# /Apply/ComfirmChannel?accessId=f4ea63d4-d849-4afd-99d4-274f06a463a9&channel=esd&fromPage=ZaEsd-Ad09
		self.s.headers["Referer"] = BASE_URL + self.confirm_product()
		url = BASE_URL + "/Apply/ComfirmChannel"
		p = {"channel": "esd"}
		param = {**self.d, **p}
		r = self.s.get(url, params=param, allow_redirects=False)
		return r.headers["Location"]

	def apply_index(self):
		"""
		详细申请第一步页面
		:param product: 产品类型，必须为符合的评估符合的产品
		:return: 返回Location
		"""
		self.s.headers["Referer"] = BASE_URL + self.confirm_product()
		url = BASE_URL + self.ComfirmChannel()
		# self.s.headers["Referer"]=access.product_referer
		r = self.s.get(url, allow_redirects=False)
		# print(self.s.cookies, 2)
		return r.headers["Location"]

	def Entrance_Assign(self):
		self.s.headers["Referer"] = BASE_URL + self.confirm_product()
		url = BASE_URL + self.apply_index()
		r = self.s.get(url, params=self.d, allow_redirects=False)
		try:
			return r.headers["Location"]
		except:
			return r.text

	def first_step_apply(self):
		url = BASE_URL+self.Entrance_Assign()
		pass


if __name__ == '__main__':
	print(DetailApply(referer).Entrance_Assign())
