# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     printsquare
   Description :
   Author :       Administrator
   date：          2018/9/8 0008
-------------------------------------------------
"""


def print_square(n):
	"""
	5(-2,-1,0,1,2)-->range(-2,3)
	:param n:
	:return:
	"""
	assert isinstance(n, int), "n must be int"
	e = -n // 2
	if n == 1:
		print("*\t*\n" * 2)
	elif n == 2:
		print("*\t" * 2, "*")
		print("*", "\t" * 2, "*")
		print("*\t" * 2, "*")
	else:
		for i in range(e, n + e + 1):
			if i == e or i == n + e:
				print("*\t" * (n + 1))
			else:
				print("*\t" + " \t" * (n - 1) + "*")


# print_square(2)

def print_number(x):
	"""
	接受一个数字字符串
	:rtype: True
	"""
	w = int("1" + (len(int(x).__str__()) - 1) * "0") #10000
	x = int(x)
	flag = False
	while w:
		t = x // w  # 4
		if flag: # false
			print(t)
		else:
			if t:
				flag = True
		x %= w
		print(x,"88")
		w //= 10
	return True


# noinspection PyTypeChecker
print_number("42000")
