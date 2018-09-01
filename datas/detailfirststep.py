# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     detailfirststep
   Description :
   Author :       Administrator
   date：          2018/9/1 0001
-------------------------------------------------
"""
from random import choice
from configs.ad09config import first_step_param
from esdwebsite.accessutil import Ad09Util
from configs.ad09config import BASE_URL
from esdwebsite.accessutil import Ad09Util


class ApplyData(object):
	def __init__(self):
		pass

	# @property
	def first_step_data(self, data=first_step_param):
		data["AccountInfo.MobilePhone"] = Ad09Util.get_mobile()
		data["AccountInfo.Email"] = Ad09Util.get_email()
		data["UserInfo.Name"] =
		data["UserInfo.EducationEnum"] = choice(range(5))
		data["UserInfo.QQNumber"] = self.qq
		data["UserInfo.IDCard"] = self.idcard
		return data
