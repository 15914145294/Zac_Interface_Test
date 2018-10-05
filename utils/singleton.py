# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     singleton
   Description :  单例模式的三种实现
   Author :       Administrator
   date：          2018/10/5 0005
-------------------------------------------------
"""
"""
单列模式：
	1) 某个类只能有一个实例
	2) 它必须自行创建这个实例
	3) 它必须自行向整个系统提供这个实例

"""

import functools


# 单例模式1
# class Singleton(object):
# 	def __new__(cls, *args, **kwargs):
# 		if not hasattr(cls, "_instance"):
# 			orign = super(Singleton, cls)
# 			cls._instance = orign.__new__(cls, *args, **kwargs)
# 		return cls._instance


# 单例模式2
# class SingletomMeta(type):
# 	def __init__(self, name, bases, dict):
# 		super(SingletomMeta, self).__init__(name, bases, dict)
# 		self._instance = None
#
# 	def __call__(self, *args, **kwargs):
# 		if self._instance is None:
# 			self._instance = super(SingletomMeta, self).__call__(*args, **kwargs)
# 		return self._instance

# 通过装饰器
def singleton(cls, *args, **kwargs):
	instances = {}

	@functools.wraps(cls)
	def _singleton():
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]

	return _singleton
