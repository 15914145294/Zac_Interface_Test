# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     second_step_apply
   Description :
   Author :       Administrator
   date：          2018/9/2 0002
-------------------------------------------------
"""
from configs.ad09config import city_value, second_step_param
from esdwebsite.detailfirststep import access
from utils.util import CommonMethods
from esdwebsite.detailfirststep import DetailApply
from esdwebsite.detailfirststep import BASE_URL
from esdwebsite.accessutil import Ad09Util


class DetailApplySecond(object):
	def __init__(self):
		self.obj = DetailApply()
		self.s = self.obj.s

	def apply4_2(self):
		result = self.obj.post_SalaryApply2()
		print(result)
		url = BASE_URL + "/apply/apply4_2"
		self.s.headers["Referer"] = url
		pattern = 'name="__RequestVerificationToken".*value="(.*?)"\s?/><input'
		token = CommonMethods.search_regular_data(result, pattern)
		data = second_step_param
		ProvinceId = city_value["广东"]
		CityId = CommonMethods.get_area_childs(ProvinceId)
		AreaId = CommonMethods.get_area_childs(CityId)
		# 设置token'
		data["__RequestVerificationToken"] = token
		# 设置省份
		data["CompanyInfo.ProvinceId"] = ProvinceId
		# 设置城市
		data["CompanyInfo.CityId"] = AreaId
		# 设置地区
		data["CompanyInfo.AreaId"] = token
		r = self.s.post(url, data=data)
		return r.text

	def apply4_3(self):
		pass

if __name__ == '__main__':
	DetailApplySecond().apply4_2()
