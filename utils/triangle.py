# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     triangle
   Description :
   Author :       Administrator
   date：          2018/10/5 0005
-------------------------------------------------
"""
"""
			[1]
		  [1][1]
		[1][2][1]
	  [1][3][3][1]
"""
n=6
oldline = []
newline = [1]
length =0
print(newline)
for i in range(1,n):
	oldline = newline.copy() # [1]
	oldline.append(0) # [1,0]
	newline.clear()
	for j in range(i+1):
		newline.append(oldline[j-1]+oldline[j])
	print(newline)