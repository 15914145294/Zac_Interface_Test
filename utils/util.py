#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : Pengbl
@Time    : 2018/5/31 17:33
@Describe: 
"""
import datetime

from logs.logUtil import logger


class UtilMethod(object):
    @staticmethod
    def read_file(file_path="", encoding="utf-8"):
        """
        读取一个文件
        :param file_path: 路径
        :param encoding: 编码
        :return: 文件中的内容
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except BaseException as e:
            print("Error: %s " % e)

    @staticmethod
    def get_time():
        """
        获取一个时间点
        :return: 返回时间点
        """
        return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    @staticmethod
    def case_argument_print(data):
        """
        case信息输出
        """
        print("|---请求详情:")
        logger.info("|---请求详情:")
        for k, v in data.items():
            print("|------%s:%s" % (k, v))
            logger.info("|------%s:%s" % (k, v))


