# encoding:utf-8

import collections
import os
from random import choice

from zac.esdwebsite.access import AccessApply
from zac.esdwebsite.simpleapply import Ad09Util
from zac.esdwebsite.costomparser import get_products
from utils.customer import customerinfo
from configs.ad09config import  check_state
from configs.config import BASE_URL, CONFIG_PATH
from zac.esdwebsite.idcard import get_idard
from utils.data import CuctomerDatautil
from utils.decoration import decorator
from utils.fileutil import CommonMethods
from utils.logUtil import logger

access = AccessApply()
# 选择产品的url
# Referer: http://uatweb.zac-esd.com/Apply/SelectProduct?accessId=1f3a403e-fba6-4c90-9463-2aa6ea38f374&frompage=ZaEsd-Ad09-
result = access.SelectProduct()
referer = BASE_URL + result[1]["location"]


class ApplyFirstStep(Ad09Util, CuctomerDatautil):
    def __init__(self):
        Ad09Util.__init__(self, "%s/ad09" % BASE_URL)
        self.d = collections.OrderedDict()
        self.a = access
        self.name = customerinfo.customername
        self.logger = logger
        self.get_access_id()
        self.idcard = customerinfo.idcard
        self.email = customerinfo.email
        self.qq = customerinfo.qq
        self.s.cookies.update(access.cookie)

    @decorator
    def get_access_id(self):
        # path_dict = self.a.EntranceAssign()
        # if isinstance(path_dict, dict):
        self.d['accessID'] = result[1]["accessid"]
        self.d['fromPage'] = result[1]["frompage"]
        return True

    @property
    def match_products(self):
        # 选择产品返回的html页面
        html = result[0]
        MATCHED_PRODUICT = get_products(html)
        if MATCHED_PRODUICT:
            return MATCHED_PRODUICT
        else:
            return None

    @decorator
    def confirm_product(self):
        """
        确认产品，产品类型用于后续的渠道确认
        :return: 返回Location，详细申请第一步
        """
        self.get_access_id()
        product = self.getProductType["ProductType"]
        p = {"productType": product}
        # self.path_dict.update(productType="salary")
        param = {**self.d, **p}
        assert product in self.match_products, "The product not matched"

        url = BASE_URL + "/Apply/ComfirmProduct"
        self.s.headers["Referer"] = referer
        r = self.s.get(url, params=param, allow_redirects=False)
        return r.headers["Location"]

    @decorator
    def SelectChannel(self):
        """
        选择产品渠道，线上，线下
        :return:
        """
        path = self.confirm_product()
        url = BASE_URL + path
        # self.s.headers["Referer"]=
        r = self.s.get(url, allow_redirects=False)
        try:
            return (url, r.text)
        except:
            return (r.text)

    @decorator
    def ComfirmChannel(self):
        """
        确认渠道
        :return:
        """
        # /Apply/ComfirmChannel?accessId=f4ea63d4-d849-4afd-99d4-274f06a463a9&channel=zac&fromPage=ZaEsd-Ad09
        self.s.headers["Referer"] = BASE_URL + self.confirm_product()
        url = BASE_URL + "/Apply/ComfirmChannel"
        p = {"channel": "esd"}
        param = {**self.d, **p}
        r = self.s.get(url, params=param, allow_redirects=False)
        return r.headers["Location"]

    @decorator
    def apply_index(self):
        """
        详细申请第一步页面
        :param product: 产品类型，必须为符合的评估符合的产品
        :return: 返回Location
        """
        self.s.headers["Referer"] = BASE_URL + self.confirm_product()
        url = BASE_URL + self.ComfirmChannel()
        # self.s.headers["Referer"]=access.product_referer
        r = self.s.get(url, allow_redirects=False)
        return r.headers["Location"]

    @decorator
    def Entrance_Assign(self):
        self.s.headers["Referer"] = BASE_URL + self.confirm_product()
        url = BASE_URL + self.apply_index()
        r = self.s.get(url, params=self.d, allow_redirects=False)
        try:
            return r.headers["Location"]
        except:
            return r.text

    def getProductApply2(self):
        self.s.headers["Referer"] = referer
        url = BASE_URL + self.Entrance_Assign()
        p = ".*assignId=(.*)&selectProductCode.*"
        p2 = 'name="__RequestVerificationToken" type="hidden" value=(.*)?"? /><input id="FromPage"'
        assignId = CommonMethods.search_regular_data(url, p)
        self.s.headers["Referer"] = referer
        # /SalaryApply2?accessId=e420c18f-21ec-405f-89c6-27f9954cb950&assignId=
        # dcb61391-c898-47b3-a108-cc848898d524&selectProductCode=Select_Product_Program_Web_Y
        # &fromPage=ZaEsd-Ad09
        r = self.s.get(url)
        text = r.text
        print("="*50)
        print(text)
        assert "__RequestVerificationToken" in text
        token = CommonMethods.search_regular_data(text, p2)
        return [assignId, token, url]

    @decorator
    def GetVoiceServicePhone(self):
        url = BASE_URL + "/Service/GetVoiceServicePhone"
        referer = BASE_URL + self.Entrance_Assign()
        self.s.headers["Referer"] = referer
        r = self.s.get(url)
        result = r.json()
        assert result["ResponseDetails"] == "ok"
        return r.json()

    @decorator
    def GetCountDownTime(self):
        url = BASE_URL + "/Service/GetCountDownTime"
        referer = BASE_URL + self.Entrance_Assign()
        self.s.headers["Referer"] = referer
        r = self.s.get(url)
        result = r.json()
        assert result["ResponseDetails"] == "ok"
        return r.json()

    @decorator
    def ValidAccountUnique(self, idcard):
        """
        检查身份证/邮箱是否唯一
        :param idcard: 身份证
        :return:
        """
        data = {"IDCard": idcard}
        url = BASE_URL + "/Validate/ValidAccountUnique"
        r = self.s.post(url, data=data)
        assert len(r.json()) == 0
        return r.json()

    @decorator
    def CheckApplyState(self, data=check_state):
        """
        检查申请状态
        :param data: 身份证，手机号，密码的dict
        :return:
        """
        result = self.getProductApply2()
        self.s.headers["Referer"] = result[-1]
        if not isinstance(data, dict):
            raise TypeError("Data msut be dict")
        assert "mobilePhone" in data and "password" in data and "idCard" in data
        data["mobilePhone"] = access.mobile
        data["idCard"] = self.idcard
        url = BASE_URL + "/apply/CheckApplyState"
        r = self.s.post(url, data=data)
        try:
            cookie = r.cookies.get_dict()
            result.append(cookie)
            assert r.json()["Code"] == 0, "申请单状态错误"
            return result
        except:
            return r.text

    @decorator
    def postProductApply2(self):
        """
        生意贷与非生意贷所掉接口不一致
        生意贷:BossApply2
        非生意贷：BossApply2
        详细申请第一步提交
        :return:
        """
        # [assignId, token,url]
        data = {}
        product_type = self.getProductType["ProductType"]
        result = self.CheckApplyState()
        # 设置referer
        # self.s.headers["Referer"] = result[2]
        # 更新cookie 因为检查申请单状态时会更新cookie
        # self.s.cookies.update(result[-1])
        # the first_step.json path
        path = "SalaryApply2"
        json_path = os.path.join(CONFIG_PATH, "first_step.json")
        if not str(product_type).startswith("boss"):
            data = CommonMethods.parse_json(json_path)["non_boss"]
        else:
            data = CommonMethods.parse_json(json_path)["boss"]
            path = "BossApply2"
        url = BASE_URL + "/{}?assignid={}".format(path, result[0])
        data["AccountInfo.MobilePhone"] = access.mobile
        data["AccountInfo.Email"] = self.email
        data["UserInfo.Name"] = access.name
        data["ApplyProduct"] = product_type
        data["UserInfo.EducationEnum"] = choice(range(5))
        data["UserInfo.QQNumber"] = self.qq
        data["UserInfo.IDCard"] = self.idcard
        # 获取省份guid
        ProvinceId = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "city.json"))["广东"]
        # 根据省份guid 获取对应城市guid
        CityId = CommonMethods.get_area_childs(ProvinceId)
        # 根据城市guid 获取区/县标识
        AreaId = CommonMethods.get_area_childs(CityId)
        data["UserInfo.ProvinceId"] = ProvinceId
        data["UserInfo.CityId"] = CityId
        data["UserInfo.AreaId"] = AreaId
        self.logger.info("身份证号码：%s",str(self.idcard))
        data["EstimateId"] = self.d["accessID"]
        data["__RequestVerificationToken"] = result[1].strip('"')
        r = self.s.post(url, data=data, allow_redirects=True)
        return r.text


# if __name__ == '__main__':
#     o = ApplyFirstStep()
#     print(o.getProductApply2())
