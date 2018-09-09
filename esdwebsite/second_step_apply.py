# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     second_step_apply
   Description :
   Author :       Administrator
   date：          2018/9/2 0002
-------------------------------------------------
"""
import os
from random import choice
from configs.config import PICTURE_PATH
from esdwebsite.detailfirststep import access
from utils.util import CommonMethods
from utils.util import CommonMethods
from esdwebsite.detailfirststep import DetailApply
from esdwebsite.detailfirststep import BASE_URL
from esdwebsite.accessutil import Ad09Util
from configs.ad09config import city_value, second_step_param, third_step_param, upload_param, upload_file_code


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
		r = self.s.post(url, data=data, allow_redirects=False)
		return r.text

	def apply_finish(self):
		self.apply4_3()
		self.s.headers["Referer"] = "{0}{1}".format(BASE_URL, "/apply/apply4_3")
		req = self.s.get("{0}{1}".format(BASE_URL, "/apply/finish"), allow_redirects=False)
		assert "/apply/Audit" in req.text
		return req.headers["Location"]

	def apply_audit(self):
		self.s.headers["Referer"] = "{baseusrl}{path}".format(baseusrl=BASE_URL, path=self.apply_finish())
		r = self.s.get("%s/apply/Audit" % BASE_URL)
		assert "系统正在审核您的贷款申请，请稍候" in r.text
		return True

	def AuditWait(self):
		if self.apply_audit():
			self.s.headers["Referer"] = "%s/apply/Audit" % BASE_URL
			r = self.s.post(BASE_URL + "/apply/AuditWait")
			try:
				assert r.json()["ResponseDetails"] == "ok", "审核异常"
				return True
			except:
				return False

	def member(self):
		if self.AuditWait():
			self.s.headers["Referer"] = "%s/apply/Audit" % BASE_URL
			r = self.s.get("%s/member" % BASE_URL)
			assert "PC会员说明" in r.text
			return True

	def RemindMessage(self):
		if self.member():
			self.s.headers["Referer"] = "%s/member" % BASE_URL
			r = self.s.post("%s/account/RemindMessage" % BASE_URL)
			assert r.json()["Status"] == 0
			session_id = self.s.cookies.get_dict()["ASP.NET_SessionId"]
			return session_id

	def upload_file(self):
		"""
		# >>> url = 'http://httpbin.org/post'
		# >>> multiple_files = [
		# ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
		# ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
		# >>> r = requests.post(url, files=multiple_files)
		:return:
		"""
		data =
		session_id = self.RemindMessage()
		self.s.headers["Content-Type"] = "multipart/form-data"
		url = BASE_URL + "/Service/AddFile"
		files = os.listdir(PICTURE_PATH)
		image = choice(files)
		picture = os.path.join(PICTURE_PATH, image)
		keys = upload_param.keys()
		for key in keys:
			if "Filename" in key:
				data[key] = picture
			elif "code" in key:
				data[key] = choice(list(upload_file_code.values()))
			elif "ASPSESSIONID" in key:
				data[key] = session_id
			elif "Filedata" in key:
				data[key % image] = upload_param[key]
			else:
				data[key] = upload_param[key]
		print(data)
		files = {'image': (image, open(picture, 'rb'), 'image/jpg')}
		r = self.s.post(url, data=data, files=files)
		print(r.text)


if __name__ == '__main__':
	print(DetailApplySecond().upload_file())
