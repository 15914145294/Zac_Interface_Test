# encoding:utf-8

import json
import os
import re

from configs.config import BASE_URL
from utils.customer import customerinfo
from configs.config import CONFIG_PATH
from zac.esdwebsite.accessutil import Ad09Util
from utils.data import CuctomerDatautil
from utils.decoration import decorator
from utils.fileutil import CommonMethods
from utils.logUtil import logger


class AccessApply(Ad09Util, CuctomerDatautil):
    def __init__(self):
        """
        初始化session 并设置header和cookie
        """
        Ad09Util.__init__(self, "%s/ad09" % BASE_URL)
        self.logger = logger
        self.name =customerinfo.customername
        self.cookie = self.result[0]
        #
        # update cookies
        #
        self.s.cookies.update(self.cookie)
        self.mobile = customerinfo.mobile
        self.logger.info("手机号码是:%s"%str(self.mobile))
        self.path_dict = dict()

        #
        # 产品Referer
        # /Apply/SelectProduct?accessId=ab9416a4-6139-4dde-9a85-520a4abed7b5&frompage=ZaEsd-Ad09-
        #
        # self.product_referer = BASE_URL + self.EntranceAssign()["location"]

        # def init_session(self):
        """
        初始化session，用于保持cookie
        :return: 返回Ad09Util类型的对象及session
        """
    @decorator
    def Ad09_index(self):
        self.s.headers.update(Referer="%s/ad09" % BASE_URL)
        param = {"__RequestVerificationToken": self.get_token(self.get_cookies()[1]),
                 "FromPage": "ZaEsd-Ad09-",
                 "FromSE": "",
                 "CustomerId": "",
                 "ProductType": "all",
                 "Amounts": 50000,
                 "LoanTerm": 24,
                 "Name": self.name,
                 "Mobile": self.mobile,
                 "Province": "31b25d9c-912d-4db9-82ab-10d87a2885b3",
                 "City": "92ce2049-36bf-4ae6-b831-22359c38f337",
                 "hiddenLoanPurpose": 0,
                 "hiddenLoanPurposeDetail": "{8132707A-E2AE-4F58-85FC-F023277D845B}"}
        r = self.s.post(self.url, data=param, allow_redirects=False)
        # print("Location url is:", r.headers["Location"])
        # /ad09/Estimate?customerId=0bcfe175-d611-41de-a9ec-0e888e9816b2&frompage=ZaEsd-Ad09-
        self.path_dict["location"] = r.headers["Location"]
        # print(self.path_dict)
        try:
            return json.loads(r.text)
        except:
            return (r.headers["Location"], r.text)

    @decorator
    def getareachilds(self):
        # self.s = self.obj[1]
        r = self.s.post("%s/service/getareachilds" % BASE_URL, allow_redirects=False)
        try:
            return r.json()
        except:
            assert isinstance(r.text, str)
            return r.text

    @decorator
    def GetLoanPurposeChilds(self):
        # self.s = self.obj[1]
        r = self.s.post("%s/service/GetLoanPurposeChilds" % BASE_URL, allow_redirects=False)
        try:
            return r.json()
        except:
            assert isinstance(r.text, str)
            return r.text

    @decorator
    def get_Estimate(self):
        # path = /ad09/Estimate?customerId=bb36179e-3687-4d2a-8fbc-fe69793d0375&frompage=ZaEsd-Ad09-'
        d = {}
        self.Ad09_index()
        path = self.path_dict["location"]
        customer_id = path.__str__().split("&")[0].split("?")[1].split("=")[1]
        url = BASE_URL + path
        d["url"] = url
        # self.s = self.obj[1]
        r = self.s.get(url)
        d["text"] = r.text
        d["customer_id"] = customer_id
        # print("The customer_id:", customer_id)
        return d

    @decorator
    def ad09_estimate(self):
        """
        简单申请，选择客户的身份：生意与非生意人士
        进行线上评估-->符合的产品
        :type product_type: non_boss,boss
        :return:
        """
        product = self.getProductType["ProductType"]
        if product == "boss_online":
            BusinessType = 0
        elif product == "boss_store":
            BusinessType = 1
        OccupationTypes = self.getProductType["OccupationTypes"]
        param = {}
        # 非生意人士
        if OccupationTypes == 0:
            param = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "access.json"))["non_boss"]
        else:
            # 生意人士
            param = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "access.json"))["boss"]
            param["BusinessType"] = BusinessType
        d = self.get_Estimate()
        url = "%s/ad09/Estimate" % BASE_URL
        # obj = self.obj[0]
        # self.s = self.obj[1]
        self.s.headers.update(Referer=d["url"])
        # 设置用户身份1为生意人士，0为非生意人士
        param["OccupationTypes"] = OccupationTypes
        param["CustomerId"] = d["customer_id"]
        param["__RequestVerificationToken"] = self.get_token(d["text"])
        r = self.s.post(url, data=param, allow_redirects=False)
        try:
            return (json.loads(r.text))
        except:
            return (r.text)

    @decorator
    def EntranceAssign(self):
        """
        申请入口，返回key包含Location,frompage,accessId，用于选择产品url
        :return:
        """
        # self.s = self.obj[1]
        # location = self.Ad09_index()[0]
        # print (BASE_URL + location,"&&&&&")
        result = self.ad09_estimate()
        self.s.headers['Referer'] = BASE_URL + self.path_dict["location"]
        path = None
        for key in dict(result).keys():
            if key.lower() == "url":
                path = result[key]
        url = BASE_URL + path
        # self.s = Ad09Util(url).s
        r = self.s.get(url, allow_redirects=False)
        location = r.headers["Location"]
        cookie = self.s.cookies.get_dict()
        # print(cookie, "**")
        assert "/Apply/SelectProduct" in r.text, "请求结果出错"
        # s =  /Apply/SelectProduct?accessId=ab9416a4-6139-4dde-9a85-520a4abed7b5&frompage=ZaEsd-Ad09-
        p = "^\/Apply.*(accessId)=(.*)\&(.*)=(.*)"
        d = {}
        try:
            m = re.compile(pattern=p).search(location).groups()
            if m:
                d[str(m[0]).lower()] = m[1]
                d[str(m[2]).lower()] = m[3]
                d["location"] = location
                d["cookie"] = cookie
                return d

            else:
                return location
        except:
            return r.text

    @decorator
    def SelectProduct(self):
        """
        返回选择产品界面，以供customparser解析符合的产品列表
        :return:
        """
        result = self.EntranceAssign()
        # print(self.s.headers)
        url = BASE_URL + result["location"]
        self.s = Ad09Util(url).s
        r = self.s.get(url, allow_redirects=False)
        return (r.text, result)

