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
from configs.config import PICTURE_PATH, BASE_API
from utils.util import CommonMethods
from utils.infoitem import InfoItems
from esdwebsite.detailfirststep import DetailApply
from esdwebsite.detailfirststep import BASE_URL
from requests_toolbelt.multipart import MultipartEncoder
from configs.ad09config import city_value, second_step_param, third_step_param, upload_param


class DetailApplySecond(object):
    def __init__(self):
        self.obj = DetailApply()
        self.s = self.obj.s
        self.n = "".join(map(lambda x: random.choice(string.digits), range(13)))

    def apply4_2(self):
        result = self.obj.post_SalaryApply2()
        url = BASE_URL + "/apply/apply4_2"
        self.s.headers["Referer"] = url
        pattern = 'name="__RequestVerificationToken".*value="(.*?)"\s?/><input'
        token = CommonMethods.search_regular_data(result, pattern)
        data = second_step_param
        ProvinceId = city_value["广东"]
        CityId = CommonMethods.get_area_childs(ProvinceId)
        AreaId = CommonMethods.get_area_childs(CityId)
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

    def apply4_3(self):
        result = self.apply4_2()
        url = BASE_URL + "/apply/apply4_3"
        self.s.headers["Referer"] = url
        data = third_step_param
        pattern = 'name="__RequestVerificationToken".*value="(.*)?"\s?/><input'
        ProvinceId = city_value["广东"]
        CityId = CommonMethods.get_area_childs(ProvinceId)
        AreaId = CommonMethods.get_area_childs(CityId)
        token = CommonMethods.search_regular_data(result, pattern)
        data["__RequestVerificationToken"] = token
        data["ContactInfo.RelativesName"] = self.obj.get_name()
        data["ContactInfo.RelativesPhone"] = self.obj.get_mobile()
        data["ContactInfo.RelativesProvinceId"] = ProvinceId
        data["ContactInfo.RelativesCityId"] = CityId
        data["ContactInfo.RelativesAreaId"] = AreaId
        data["ContactInfo.ColleagueName"] = self.obj.get_name()
        data["ContactInfo.ColleaguePhone"] = self.obj.get_mobile()
        data["ContactInfo.OtherRelativesName"] = self.obj.get_name()
        data["ContactInfo.OtherRelativesPhone"] = self.obj.get_mobile()
        r = self.s.post(url, data=data, allow_redirects=False)
        return r.text

    def apply_finish(self):
        self.apply4_3()
        self.s.headers["Referer"] = "{0}{1}".format(BASE_URL, "/apply/apply4_3")
        req = self.s.get("{0}{1}".format(BASE_URL, "/apply/finish"), allow_redirects=False)
        assert "/apply/Audit" in req.text
        return req.headers["Location"]

    def apply_audit(self):
        self.s.headers["Referer"] = "{baseusrl}{path}".format(baseusrl=BASE_URL, path=self.apply_finish())
        r = self.s.get("%s/apply/Audit" % BASE_URL)
        assert "系统正在审核您的贷款申请，请稍候" in r.text
        return True

    def AuditWait(self):
        if self.apply_audit():
            self.s.headers["Referer"] = "%s/apply/Audit" % BASE_URL
            r = self.s.post(BASE_URL + "/apply/AuditWait")
            try:
                assert r.json()["ResponseDetails"] == "ok", "审核异常"
                return True
            except:
                return False

    def member(self):
        result=self.AuditWait()
        if not result:
            return False
        self.s.headers["Referer"] = "%s/apply/Audit" % BASE_URL
        r = self.s.get("%s/member" % BASE_URL)
        assert "PC会员说明" in r.text
        info_items = InfoItems(r.text).parser_code()
        return info_items

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
    #     print(r.text)

    def RemindMessage(self):
        items=self.member()
        self.s.headers["Referer"] = "%s/member" % BASE_URL
        r = self.s.post("%s/account/RemindMessage" % BASE_URL)
        assert r.json()["Status"] == 0
        session_id = self.s.cookies.get_dict()["ASP.NET_SessionId"]
        return session_id, items

    # POST /Information/UploadDialog?code=1.1&random=1537325899379
    def UploadDialog(self):
        result = self.RemindMessage()
        code = choice(list(result[1].values()))
        number = self.n
        data = {}
        data["code"] = code
        data["random"] = number
        r = self.s.post(BASE_URL + "/Information/UploadDialog", params=data)
        assert "请确保信息的真实性" in r.text
        return result

    # /Tools/uploadify/uploadify.swf
    def uploadify(self):
        params = {"preventswfcaching": self.n}
        if self.UploadDialog():
            r = self.s.get(BASE_URL + "/Tools/uploadify/uploadify.swf", params=params)
        return r.text.encode("utf-8").decode("utf-8")

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

    def upload_file(self):
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
        files = os.listdir(PICTURE_PATH)
        filename = choice(files)
        file_path = os.path.join(PICTURE_PATH, filename)
        ret = self.UploadDialog()
        for code in list(ret[1].values()):
            multipart_encoder = MultipartEncoder(
                fields={
                    "Filename": filename,
                    # "code": choice(list(upload_file_code.values())),
                    "code": code,
                    "ASPSESSIONID": ret[0],
                    "Filedata": (filename, open(file_path, 'rb'), 'application/octet-stream')
                },
                boundary="------------------------" + str(random.randint(1e28, 1e29 - 1)),
                encoding='utf-8'
            )
            self.s.headers["Content-Type"] = multipart_encoder.content_type
            r = self.s.post(url, data=multipart_encoder, )
            results = r.json()
            if results["ResponseDetails"] == "ok":
                continue
            else:
                raise AssertionError("上传图片出现异常")
        return True


if __name__ == '__main__':
    print(DetailApplySecond().upload_file())
