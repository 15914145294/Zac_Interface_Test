#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from utils.file_read import YamlReader

# 根路径
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# 配置文件路径
CONFIG_FILE = os.path.join(BASE_PATH, 'configs', 'config.yml')
# 数据路径
DATA_PATH = os.path.join(BASE_PATH, 'data')
# log文件路径
LOG_PATH = os.path.join(BASE_PATH, 'logs')
# config文件路径
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')
# 报告文件路径
REPORT_PATH = os.path.join(BASE_PATH, 'reports')
# CASE路径
CASE_PATH = os.path.join(BASE_PATH, 'testcases')
# 名的配置路径
FIRST_NAME =os.path.join(BASE_PATH, 'configs', 'first_names.json')
# 姓的配置路径
LAST_NAME = os.path.join(BASE_PATH, 'configs', 'last_names.json')
BASE_URL="http://uatweb.zac-esd.com"


class Config(object):
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，
        第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。
        可以在框架中实现多个项目的测试。
        """
        return self.config[index].get(element)
