# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     second_step_apply
   Description :
   Author :       Administrator
   date：          2018/9/2 0002
-------------------------------------------------
"""
import os
import random
import string
from random import choice
from utils.decoration import decorator
from utils.data import ConfigDatautil
from configs.config import PICTURE_PATH
from utils.fileutil import CommonMethods
from utils.items import InfoItems
from esdwebsite.detailfirststep import ApplyFirstStep
from configs.config import BASE_URL, CONFIG_PATH
from requests_toolbelt.multipart import MultipartEncoder


class DetailApply(ConfigDatautil):
    def __init__(self):
        self.obj = ApplyFirstStep()
        self.s = self.obj.s
        # the user name
        self.name = self.obj.name
        self.n = "".join(map(lambda x: random.choice(string.digits), range(13)))

    @decorator
    def getParamStructure(self, config_name):
        d = {}
        product_type = self.getProductType["ProductType"]
        try:
            json_path = os.path.join(CONFIG_PATH, config_name)
        except:
            raise ValueError("详细申请配置文件不存在")
        data = CommonMethods.parse_json(json_path)["non_boss"]
        path = ""
        occupationtypes = ""
        if str(config_name).startswith("second"):
            if str(product_type).startswith("boss"):
                path = "applyboss1_2"
                data = CommonMethods.parse_json(json_path)["boss"]
                occupationtypes = 1
            else:
                path = "apply4_2"
                data = CommonMethods.parse_json(json_path)["non_boss"]
                occupationtypes = 0
        elif str(config_name).startswith("third"):
            if str(product_type).startswith("boss"):
                path = "applyboss1_3"
                data = CommonMethods.parse_json(json_path)["boss"]
                occupationtypes = 1
            else:
                path = "apply4_3"
                data = CommonMethods.parse_json(json_path)["non_boss"]
                occupationtypes = 0
        d["path"] = path
        d["data"] = data
        d["OccupationTypes"] = occupationtypes
        return d

    @decorator
    def apply4_2(self):
        """
        详细申请第二步
        老板贷调用接口:/applyboss1_2
        非老板贷调用接口：apply4_2
        :return:
        """
        # 获取详细申请第一步后的结果
        result = self.obj.postProductApply2()
        ret = self.getParamStructure("second_step.json")
        data = ret["data"]
        path = ret["path"]
        # 构造请求地址
        url = BASE_URL + "/apply/{}".format(path)
        self.s.headers["Referer"] = url
        pattern = '"__RequestVerificationToken".*?value=\n?"(.+?)"'
        token = CommonMethods.search_regular_data(result, pattern)
        # 获取省份guid
        ProvinceId = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "city.json"))["广东"]
        # 根据省份guid 获取对应城市guid
        CityId = CommonMethods.get_area_childs(ProvinceId)
        # 根据城市guid 获取区/县标识
        AreaId = CommonMethods.get_area_childs(CityId)
        # 获取申请单号
        p = r'.*ApplyId"\n?.*=(".*?")/>'
        applyid = CommonMethods.search_regular_data(result, p)
        if applyid:
            data["EnterpriseInfo.ApplyId"] = applyid
            # 设置公司省份
            data["EnterpriseInfo.ProvinceId"] = ProvinceId
            data["EnterpriseInfo.CityId"] = CityId
            data["EnterpriseInfo.AreaId"] = AreaId
        if ret["OccupationTypes"]==0:
            data["CompanyInfo.Type"]=random.choice(range(9))
        # 设置token'
        data["__RequestVerificationToken"] = token
        # 设置省份
        data["CompanyInfo.ProvinceId"] = ProvinceId
        # 设置城市
        data["CompanyInfo.CityId"] = CityId
        # 设置地区
        data["CompanyInfo.AreaId"] = AreaId
        r = self.s.post(url, data=data)
        return r.text

    @decorator
    def apply4_3(self):
        """
        详细申请第三步：联系人资料
        生意贷与非生意贷调用接口不一致
        生意贷：applyboss1_3
        非生意贷：apply4_3
        :return:
        """
        # path = "apply4_3"
        result = self.apply4_2()
        ret = self.getParamStructure("third_step.json")
        data = ret["data"]
        path = ret["path"]
        # 构造请求地址
        url = BASE_URL + "/apply/{}".format(path)
        pattern = '"__RequestVerificationToken".*?value=\n?"(.+?)"'
        token = CommonMethods.search_regular_data(result, pattern)
        ProvinceId = CommonMethods.parse_json(os.path.join(CONFIG_PATH, "city.json"))["广东"]
        CityId = CommonMethods.get_area_childs(ProvinceId)
        AreaId = CommonMethods.get_area_childs(CityId)
        if ret["OccupationTypes"] == 1:
            data["ContactInfo.BusinessPartner"] = self.obj.get_name()
            data["ContactInfo.PartnerMobile"] = self.obj.get_mobile()
        data["__RequestVerificationToken"] = token
        data["ContactInfo.RelativesName"] = self.obj.get_name()
        data["ContactInfo.RelativesPhone"] = self.obj.get_mobile()
        if ret["OccupationTypes"]==0:
            data["ContactInfo.RelativesProvinceId"] = ProvinceId
            data["ContactInfo.RelativesCityId"] = CityId
            data["ContactInfo.RelativesAreaId"] = AreaId
            data["ContactInfo.ColleagueName"] = self.obj.get_name()
            data["ContactInfo.ColleaguePhone"] = self.obj.get_mobile()
        data["ContactInfo.OtherRelativesName"] = self.obj.get_name()
        data["ContactInfo.OtherRelativesPhone"] = self.obj.get_mobile()
        r = self.s.post(url, data=data, allow_redirects=False)
        return r.text

    @decorator
    def apply_finish(self):
        self.apply4_3()
        self.s.headers["Referer"] = "{0}{1}".format(BASE_URL, "/apply/%s")\
                                    %(self.getParamStructure("third_step.json")["path"])
        req = self.s.get("{0}{1}".format(BASE_URL, "/apply/finish"), allow_redirects=False)
        assert "/apply/Audit" in req.text
        return req.headers["Location"]

    @decorator
    def apply_audit(self):
        self.s.headers["Referer"] = "{baseusrl}{path}".format(baseusrl=BASE_URL, path=self.apply_finish())
        r = self.s.get("%s/apply/Audit" % BASE_URL)
        assert "系统正在审核您的贷款申请，请稍候" in r.text
        return True

    @decorator
    def AuditWait(self):
        if self.apply_audit():
            self.s.headers["Referer"] = "%s/apply/Audit" % BASE_URL
            r = self.s.post(BASE_URL + "/apply/AuditWait")
            try:
                assert r.json()["ResponseDetails"] == "ok", "审核异常"
                return True
            except:
                return False

    @decorator
    def member(self):
        """
        获取请求结果，并将返回的页面解析，获取需要上传的资料项
        :return: 返回需要的上传资料项包括加分项以及用于上传资料完成后提交的token信息
        """
        d = {}
        result = self.AuditWait()
        if not result:
            return False
        self.s.headers["Referer"] = "%s/apply/Audit" % BASE_URL
        r = self.s.get("%s/member" % BASE_URL)
        assert "PC会员说明" in r.text
        info_items = InfoItems(r.text).parser_code()
        pattern = r'type="hidden"\n?.*value="(.*)?" /> '
        token = CommonMethods.search_regular_data(r.text, pattern)
        d["items"] = info_items
        d["token"] = token
        return d

    # def GetInfoItems(self):
    #     result = self.member()
    #     self.s.headers["Authorization"] = "Bearer buLeqCMjUZweS8wBSV8C4gCSZ06UeF7dErH_VYuF" \
    #                                       "xuNthWTsi8opr0pjVxIe6-AgVuS6xGQ86Z04rm80ELIy" \
    #                                       "WICdafRUCXU9f6ph_Wk1L76dpIgdrkHfAvdbSRGVvONmBt" \
    #                                       "YDzyquVOE1ORfq1hQZNo99RN_RicCYvyNhklm1RdOplUZRIi" \
    #                                       "6QkEkaKoeZEpr0k3imnZ3qQJUJXn0qhJQb17KtpYZMSWf" \
    #                                       "UNR0bP1xLBgDXiJ-YM1eVj0dGb6nmP7yuEb7HtA"
    #     url = BASE_API + "/api/v2/Information/GetInfoItems"
    #     r = self.s.get(url)
    @decorator
    def RemindMessage(self):
        # ret is a dict:{"items":info_items,"token":token}
        ret = self.member()
        self.s.headers["Referer"] = "%s/member" % BASE_URL
        r = self.s.post("%s/account/RemindMessage" % BASE_URL)
        assert r.json()["Status"] == 0
        session_id = self.s.cookies.get_dict()["ASP.NET_SessionId"]
        ret.update(session=session_id)
        return ret

        # POST /Information/UploadDialog?code=1.1&random=1537325899379

    @decorator
    def UploadDialog(self):
        ret = self.RemindMessage()
        code = choice(list(ret["items"].values()))
        number = self.n
        data = {}
        data["code"] = code
        data["random"] = number
        r = self.s.post(BASE_URL + "/Information/UploadDialog", params=data)
        assert "请确保信息的真实性" in r.text
        return ret

    # /Tools/uploadify/uploadify.swf
    @decorator
    def uploadify(self):
        params = {"preventswfcaching": self.n}
        if self.UploadDialog():
            r = self.s.get(BASE_URL + "/Tools/uploadify/uploadify.swf", params=params)
        return r.text.encode("utf-8").decode("utf-8")

    @decorator
    def parse_upload_information(self):
        """
        <td class="name">
            <span class="red">*</span>
            <span style="margin-left: 10px;">授权委托书</span>
            <a href="javascript:void(0);" style="color: #E87B26; text-decoration: none;" onclick="ajaxLoadHtml(this,
             '/Information/UploadDesc?code=1.3');">资料要求</a>
        1)找出所有需要上传的资料项
        2）解析a标签中的code
        3）解析资料项，获取资料项名称
        4）将资料项及code组合成对应的字典
        :return:
        """
        pass

    @decorator
    def upload_files(self):
        """
        # >>> url = 'http://httpbin.org/post'
        # >>> multiple_files = [
        # ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
        # ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
        # >>> r = requests.post(url, files=multiple_files)
        :return:
        """
        """
        1)找出所有需要上传的资料项
        2)循环上传所有的资料
        """
        url = BASE_URL + "/Service/AddFile"
        data = {}
        # get the file of path
        files = os.listdir(PICTURE_PATH)
        filename = choice(files)
        file_path = os.path.join(PICTURE_PATH, filename)
        ret = self.UploadDialog()
        for code in list(ret["items"].values()):
            multipart_encoder = MultipartEncoder(
                fields={
                    "Filename": filename,
                    # "code": choice(list(upload_file_code.values())),
                    "code": code,
                    "ASPSESSIONID": ret["session"],
                    "Filedata": (filename, open(file_path, 'rb'), 'application/octet-stream')
                },
                boundary="------------------------" + str(random.randint(1e28, 1e29 - 1)),
                encoding='utf-8'
            )
            # the content type is:multipart/form-data; boundary={0}
            self.s.headers["Content-Type"] = multipart_encoder.content_type
            r = self.s.post(url, data=multipart_encoder, )
            results = r.json()
            if results["ResponseDetails"] == "ok":
                continue
            else:
                raise AssertionError("上传图片出现异常")
        return ret

    @decorator
    def UpLoadCompleted(self):
        """
        上传资料后，进行资料项提交
        资料提交后，会重定向到"/Member"页面
        :return:/Member".text用于获取其中的token
        """
        # get the token
        ret = self.upload_files()
        try:
            token = ret["token"]
        except KeyError:
            raise ("token信息不存在")
        # Content-Type: application/x-www-form-urlencoded
        # change the content-type of session
        self.s.headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {"__RequestVerificationToken": token}
        result = self.s.post(url=BASE_URL + "/Information/UpLoadCompleted", data=data)
        # 请求成功后，会重定向到BASE_URL+"/Member"
        assert r"持卡人" in result.text
        return result.text

# if __name__ == '__main__':
#     print(DetailApply().UpLoadCompleted())
