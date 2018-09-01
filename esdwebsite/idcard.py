# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     idcard
   Description :  生成身份证，检查是否是身份证
   Author :       Administrator
   date：          2018/8/26 0026
-------------------------------------------------
"""
import re
import random
from datetime import datetime, timedelta, date
from esdapi.idcard_area_code import area_code_dict

id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]


def is_id_card(idcard):
	if len(idcard) != 18:
		return False, "Length error"
	if not re.match(r"^\d{17}(\d|X|x)$", idcard):
		return False, "Format error"
	if idcard[0:6] not in area_code_dict:
		return False, "Area code error"
	try:
		date(int(idcard[6:10]), int(idcard[10:12]), int(idcard[12:14]))
	except ValueError as ve:
		return False, "Datetime error: {0}".format(ve)
	if str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in idcard[0:-1]])]) % 11]) != \
			str(idcard.upper()[-1]):
		return False, "Check code error"
	return True, "{}省 {}市 {}".format(area_code_dict[idcard[0:2] + "0000"].rstrip("省"),
	                                 area_code_dict[idcard[0:4] + "00"].rstrip("市"),
	                                 area_code_dict[idcard[0:6]])


def make_idcard(area_code, age, gender):
	if str(area_code) not in area_code_dict.keys():
		return None
	#
	# 根据age 随机生成对应的出生日期字符串
	#
	datestring = str(date(date.today().year - age, 1, 1) + timedelta(days=random.randint(0, 364))).replace("-", "")
	print(datestring)
	rd = random.randint(0, 999)
	if gender == 0:
		gender_num = rd if rd % 2 == 0 else rd + 1
	else:
		gender_num = rd if rd % 2 == 1 else rd - 1
	result = str(area_code) + datestring + str(gender_num).zfill(3)
	return result + str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 11])


def get_idard(age, gender):
	if not isinstance(age, int):
		raise ValueError("Age must be integer")
	assert gender in [0, 1], "The gender must be  0 or 1"
	codes = area_code_dict.keys()
	area_code = random.choice(list(codes))
	id_number = make_idcard(int(area_code), age, gender)
	return id_number


# if __name__ == "__main__":
# 	id_number = get_idard(22, 1)
# 	print(id_number)
# 	print(is_id_card(id_number))
