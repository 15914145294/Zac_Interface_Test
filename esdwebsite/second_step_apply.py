# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     second_step_apply
   Description :
   Author :       Administrator
   date：          2018/9/2 0002
-------------------------------------------------
"""
from configs.ad09config import city_value, second_step_param, third_step_param
from esdwebsite.detailfirststep import access
from utils.util import CommonMethods
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
		data["CompanyInfo.CityId"] = CityId
		# 设置地区
		data["CompanyInfo.AreaId"] = AreaId
		r = self.s.post(url, data=data)
		return r.text

	def apply4_3(self):
		result = self.apply4_2()
		url = BASE_URL + "/apply/apply4_3"
		self.s.headers["Referer"] = url
		data = third_step_param
		pattern = 'name="__RequestVerificationToken".*value="(.*)?"\s?/><input'
		ProvinceId = city_value["广东"]
		CityId = CommonMethods.get_area_childs(ProvinceId)
		AreaId = CommonMethods.get_area_childs(CityId)
		token = CommonMethods.search_regular_data(result, pattern)
		data["__RequestVerificationToken"] = token
		data["ContactInfo.RelativesName"] = self.obj.get_name()
		data["ContactInfo.RelativesPhone"] = self.obj.get_mobile()
		data["ContactInfo.RelativesProvinceId"] = ProvinceId
		data["ContactInfo.RelativesCityId"] = CityId
		data["ContactInfo.RelativesAreaId"] = AreaId
		data["ContactInfo.ColleagueName"] = self.obj.get_name()
		data["ContactInfo.ColleaguePhone"] = self.obj.get_mobile()
		data["ContactInfo.OtherRelativesName"] = self.obj.get_name()
		data["ContactInfo.OtherRelativesPhone"] = self.obj.get_mobile()
		r = self.s.post(url, data=data,allow_redirects=False)
		print(r.text)


if __name__ == '__main__':
	DetailApplySecond().apply4_3()
