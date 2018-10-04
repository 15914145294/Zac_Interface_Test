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

class Test(object):
	def __init__(self):
		print("__init__ test")

	def __call__(self, *args, **kwargs):
		print("__call__ test")

t= Test()
t()
