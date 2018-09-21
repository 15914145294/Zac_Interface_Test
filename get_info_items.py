# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: infoitem.py
@time: 2018/09/21 
"""
import os
from bs4 import BeautifulSoup


class InfoItems(object):
    def __init__(self, html):
        try:
            with open(html, "rb") as f:
                self.soup = BeautifulSoup(f, 'html.parser')
        except:
            self.soup = BeautifulSoup(html, 'html.parser')
        self.data = []
        self.code = []

    def parser_code(self):
        # Perform a CSS selection operation on the current element
        d = {}
        items = self.soup.select("td.name  span[style='margin-left: 10px;']")
        codes = self.soup.select("td.name  span[style='margin-left: 10px;'] + a")
        for item in items:
            self.data.append(item.string)
        for code in codes:
            self.code.append(str(code["onclick"]).strip("');").split("=")[-1])
        for i in zip(self.data, self.code):
            d[i[0]] = i[1]
        for value in list(d.values()):
            if value=="1.1":
                d.__delitem__("身份证正反面")
                d.update(身份证正面=value)
                d.update(身份证反面=value)
        return d


# if __name__ == "__main__":
#     print(InfoItems("infoitem.html").parser_code())
