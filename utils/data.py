# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: data.py 
@time: 2018/09/28 
"""
import os
from configs.config import ConfigENum
from utils.file_read import YamlReader


class ConfigDatautil(object):
    def __init__(self):
        object.__init__(self)

    @property
    def getProductType(self):
        """
        获取产品类型及用户身份：生意人士，非生意人士
        such as：
            {'OccupationTypes': 1, 'ProductType': 'boss_store'}
        :return:包含产品类型及用户身份的dict
        """
        yml_path = os.path.join(ConfigENum.CONFIG_PATH.value, "config.yml")
        data = YamlReader(yml_path).data[0]["product"]
        return data


if __name__ == "__main__":
    pass
