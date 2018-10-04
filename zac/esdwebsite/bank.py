# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: bank.py 
@time: 2018/09/26 
"""
import os
import random
import time
import string, traceback
from utils.DB import MysqlDb
from utils.logUtil import logger
from utils.decoration import decorator
from utils.dictionary import DictUtil
from utils.fileutil import CommonMethods
from zac.esdwebsite.detailapply import DetailApply, customerinfo
from requests_toolbelt.multipart import MultipartEncoder
from configs.config import BASE_URL, CONFIG_PATH, VIDEO_PATH


class BankVideo(object):
	def __init__(self):
		self.obj = DetailApply()
		self.s = self.obj.s
		self.logger = logger

	def getBankCode(self):
		"""
		随机生成18号码的中国银行
		:return:
		"""
		prefix = "621666"
		suffix = "".join(map(lambda x: random.choice(string.digits), range(12)))
		return int(prefix + suffix)

	def dump_customerinfo(self):
		SQL = """INSERT into apply_info(id,mobile,idcard,customername,create_date) \
               VALUES('%s','%s','%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))""" \
		      % (
			      customerinfo.applyid, customerinfo.mobile,
			      customerinfo.idcard, customerinfo.
				      customername, customerinfo.create_date)
		logger.info("sql is:%s" % SQL)
		with MysqlDb() as db:
			try:
				db.execute(SQL)
				return True
			except:
				error_message = traceback.format_exc()
				logger.error(error_message)
				return False

	@decorator
	def bind_bank(self):
		"""
		详细申请三步提交后，绑定银行卡
		:return:
		"""
		text = self.obj.UpLoadCompleted()
		pattern = r'name="__RequestVerificationToken" type="hidden"\n?.*value="(.*)?" />'
		# get the token
		token = CommonMethods.search_regular_data(text, pattern)
		bank_path = os.path.join(CONFIG_PATH, "bank.json")
		bank_name = "中国银行"
		# 获取开户银行
		bank_guid = CommonMethods.parse_json(bank_path)["bank"][bank_name]
		data = CommonMethods.parse_json(bank_path)["param"]
		# 获取开户行所在地
		city_path = os.path.join(BASE_URL, "city.json")
		province_d = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "city.json"))
		ProvinceId = province_d["广东"]
		city_d = CommonMethods.get_city(ProvinceId)
		# 根据省份guid 获取对应城市guid
		CityId = CommonMethods.get_area_childs(ProvinceId)
		# 获取银行卡号
		ProvinceName = DictUtil.get_key(province_d, ProvinceId)
		CityName = DictUtil.get_key(city_d, CityId)
		bank_account = self.getBankCode()
		data["__RequestVerificationToken"] = token
		data["Name"] = self.obj.name
		data["SelectedBank"] = bank_name
		data["Code"] = bank_guid
		data["ProvinceId"] = ProvinceId
		data["CityId"] = CityId
		data["BankAccount"] = bank_account
		data["BankLocation"] = "{}省 {}".format(ProvinceName, CityName)
		self.logger.info("请求参数是%s" % str(data))
		self.s.headers["Referer"] = BASE_URL + "/member"
		r = self.s.post(BASE_URL + "/BankCard/Bind", data=data, allow_redirects=False)
		session = self.s.cookies.get_dict()["ASP.NET_SessionId"]
		assert r"/member" in r.text
		# self.dump_customerinfo()
		return session

	@decorator
	def videoUpload(self):
		# get the video path
		session_id = self.bind_bank()
		path = os.path.join(VIDEO_PATH, "test_video.mp4")
		multipart_encoder = MultipartEncoder(
			fields={
				"Filename": "test_video.mp4",
				# "code": choice(list(upload_file_code.values())),
				"ASPSESSIONID": session_id,
				"Filedata": ("test_vedio.mp4", open(path, 'rb'), 'application/octet-stream')
			},
			boundary="------------------------" + str(random.randint(1e28, 1e29 - 1)),
			encoding='utf-8'
		)
		self.s.headers["Content-Type"] = multipart_encoder.content_type
		r = self.s.post(BASE_URL + "/Video/VideoUploadService", data=multipart_encoder, )
		assert "ok" in r.text
		self.dump_customerinfo()
		return True


if __name__ == "__main__":
	print(BankVideo().videoUpload())
