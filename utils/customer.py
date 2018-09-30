# -*- coding:utf-8 _*-
""" 
@author:Administrator 
@file: customer.py 
@time: 2018/09/30 
"""
"""
保存客户信息，用于后期数据持久化操作
"""
import time
from zac.esdwebsite.idcard import get_idard
from utils.data import CuctomerDatautil as customer


class CustomerInfo(object):
    __slots__ = (
        "id", "mobile", "idcard",
        "customername", "create_date", "__dict__",
        "qq","email","applyid"
    )

    def __init__(self):
        object.__init__(self)

    def __setattr__(self, k, v):
        if k == "mobile":
            if not isinstance(v, int):
                raise TypeError("Value must be int")
        self.__dict__[k] = v

    def __getattr__(self, item):
        """
        调用不存在的属性时触发
        :param item:
        :return:
        """
        try:
            return self.__dict__[item]
        except:
            return item + ' is not found!'

    def __delattr__(self, item):
        try:
            del self.__dict__[item]
        except:
            return item + ' is not found!'

    def __str__(self):
        try:
            return {"id": self.__dict__["id"],
                    "mobile": self.__dict__["mobile"],
                    "idcard": self.__dict__["idcard"],
                    "customername": self.__dict__["customername"]}.__str__()
        except:
            return self.__dict__.__str__()

    __repr__ = __str__

# set customerinfo
day = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
customerinfo = CustomerInfo()
customerinfo.customername = customer.get_name()
customerinfo.idcard = get_idard(28, 1)
customerinfo.email = customer.get_email()
customerinfo.qq = customer.get_QQNumber()
customerinfo.mobile = customer.get_mobile()
customerinfo.create_date = day

