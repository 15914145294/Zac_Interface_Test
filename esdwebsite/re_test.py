# encoding:utf-8


import re

s = "/Apply/SelectProduct?accessId=ab9416a4-6139-4dde-9a85-520a4abed7b5&frompage=ZaEsd-Ad09-"
p = "^\/Apply.*(accessId)=(.*)\&(.*)=(.*)"

p = re.compile(p)
m = p.search(s).groups()
print(m)
