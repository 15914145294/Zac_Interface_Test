# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       Administrator
   date：          2018/9/8 0008
-------------------------------------------------
"""
import os
from random import  choice
from configs.config import PICTURE_PATH
from configs.ad09config import upload_param
data = {}
keys = upload_param.keys()
print(list(keys))
for i in keys:
	for key in keys:
		if "Filename" in key:
			data[key] = "02.jpg"
		elif "code" in key:
			data["key"] = "1.1"
		elif "ASPSESSIONID" in key:
			data[key] = "dfgdgdgd"
		else:
			data[key] = upload_param[key]
print(data)


