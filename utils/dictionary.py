# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: dictionary.py 
@time: 2018/09/26 
"""
# import os
# from utils.fileutil import CommonMethods,CONFIG_PATH

class DictUtil(object):
    @staticmethod
    def get_key(dict, value):
        value=[k for k, v in dict.items() if v == value]
        return value[0]

# province_d = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "city.json"))
# value=DictUtil.get_key(province_d,"31b25d9c-912d-4db9-82ab-10d87a2885b3")
# print(value)
