# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: decoration.py 
@time: 2018/09/27 
"""
import traceback
from functools import wraps
from utils.logUtil import logger
from configs.config import CONFIG_PATH
from utils.file_read import YamlReader


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("-" * 20 + "request start" + "-" * 20)
        try:
            result = func(*args, **kwargs)
            logger.info("%s 请求结果是：%s" % (func.__name__, result))
        except:
            error_message = traceback.format_exc()
            logger.error("%s 请求出错：%s" % (func.__name__, error_message))
        return result

    return wrapper


if __name__ == "__main__":
    pass
