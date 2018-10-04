# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     enumeration
   Description :
   Author :       Administrator
   date：          2018/10/4 0004
-------------------------------------------------
"""
from enum import Enum, unique

# Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
#
# for name, member in Month.__members__.items():
# 	print(name, '=>', member, ',', member.value)

# from enum import Enum, unique
#
# @unique
# class Weekday(Enum):
#     Sun = 0 # Sun的value被设定为0
#     Mon = 1
#     Tue = 2
#     Wed = 3
#     Thu = 4
#     Fri = 5
#     Sat = 6
# print(Weekday.Sat.value)

from enum import Enum, unique


@unique
class Gender(Enum):
	Male = "m"
	Female = "w"


class Student(object):
	def __init__(self, name, gender):
		self.name = name
		if type(gender) == Gender:
			self.gender = gender
		else:
			raise ValueError('gender type error')

	def __str__(self):
		return '学生的姓名为：%s,性别为：%s' % (self.name, self.gender)

	__repr__ = __str__


if __name__ == '__main__':
	print(Student('mike', Gender.Female))
	print(Student('LiLi', Gender.Male))
