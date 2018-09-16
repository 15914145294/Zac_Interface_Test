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

def human(size:int):
	units = ["","K","M","G","T"]
	depth = 0
	while size>=1024:
		size = size // 1024
		depth+=1
	return "{}{}".format(size,units[depth])

print(human(1024))
print(human(1024000))
print(human(102400000))
print(human(10240000000))