# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ad09config
   Description :  简单申请的相关配置信息
   Author :       Administrator
   date：          2018/9/1 0001
-------------------------------------------------
"""

BASE_URL = "http://uatweb.zac-esd.com"

ESD_PRODUCTS = ["boss",
                "boss_mt1",
                "boss_mt2",
                "boss_online",
                "boss_store",
                "fangrongdai",
                "mortgage",
                "owner",
                "primary_boss",
                "quickloan_salary",
                "quickloan_salary_shebao",
                "quickloan_shebao",
                "salary",
                "salary_teacher",
                "shebao",
                "suixindai",
                "suixindaiboss",
                "suixindaisalary",
                "toujiadai",
                "yifangdai",
                "yinyetong",
                "zhongxin"]

# 详细申请第一步提交参数
first_step_param = {"__RequestVerificationToken": "token",
                    "FromPage": "WebSite-Apply4",
                    "UserInfo.FromPage": "WebSite-Apply4",
                    "ApplyProduct": "salary",
                    # accessid
                    "EstimateId": "1f3a403e-fba6-4c90-9463-2aa6ea38f374",
                    "AccountInfo.MobilePhone": "",
                    "AccountInfo.PassWord": "123456a",
                    "AccountInfo.ConfirmPassWord": "123456a",
                    "Amounts": 30000,
                    "DeadlineEnum": 24,
                    "UserInfo.Name": "",
                    # idcard
                    "UserInfo.IDCard": "",
                    "UserInfo.MaritalEnum": 0,
                    # 子女数
                    "UserInfo.ChildNumber": 0,
                    "UserInfo.AreaCode": "",
                    "UserInfo.Telephone": "",
                    "AccountInfo.Email": "",
                    # 教育程度
                    "UserInfo.EducationEnum": 1,
                    "UserInfo.QQNumber": "",
                    "UserInfo.AccountEnum": 0,
                    "UserInfo.LiveEnum": 1,
                    "UserInfo.ProvinceId": "31b25d9c-912d-4db9-82ab-10d87a2885b3",
                    "UserInfo.CityId": "92ce2049-36bf-4ae6-b831-22359c38f337",
                    "UserInfo.AreaId": "5e70992c-e188-4712-8009-e1049b2513a6",
                    # 居住地址
                    "UserInfo.Address": "景德镇",
                    "UserInfo.InfoSource": 4}
