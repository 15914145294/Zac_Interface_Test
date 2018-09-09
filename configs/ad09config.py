# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ad09config
   Description :  简单申请的相关配置信息
   Author :       Administrator
   date：          2018/9/1 0001
-------------------------------------------------
"""
from random import choice

BASE_URL = "http://"

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
# 检查申请状态参数
check_state = {
	"mobilePhone": 14415333442,
	"password": "123456a",
	"idCard": "430523199605192117"
}

# 详细申请第一步提交参数
first_step_param = {
	"__RequestVerificationToken": "token",
	"FromPage": "WebSite-Apply4",
	"UserInfo.FromPage": "WebSite-Apply4",
	"ApplyProduct": "salary",
	"EstimateId": "",
	"AccountInfo.MobilePhone": "",
	"AccountInfo.PassWord": "123456a",
	"AccountInfo.ConfirmPassWord": "123456a",
	"Amounts": 30000,
	"DeadlineEnum": 24,
	"UserInfo.Name": "",
	"UserInfo.IDCard": "",
	"UserInfo.MaritalEnum": 0,
	"UserInfo.ChildNumber": 0,
	"UserInfo.AreaCode": "",
	"UserInfo.Telephone": "",
	"AccountInfo.Email": "",
	"UserInfo.EducationEnum": 1,
	"UserInfo.QQNumber": "",
	"UserInfo.AccountEnum": 0,
	"UserInfo.LiveEnum": 1,
	"UserInfo.ProvinceId": "31b25d9c-912d-4db9-82ab-10d87a2885b3",
	"UserInfo.CityId": "92ce2049-36bf-4ae6-b831-22359c38f337",
	"UserInfo.AreaId": "5e70992c-e188-4712-8009-e1049b2513a6",
	"UserInfo.Address": "景德镇",
	"UserInfo.InfoSource": 4
}

city_value = {
	"北京": "7cd64271-5e1e-413c-8420-0f2a4899de8e",
	"天津": "6a4c191d-38bc-4c7e-9326-68f614e49860",
	"河北": "a704a4aa-42c2-4901-beab-535949ded7bf",
	"山西": "82778f8e-38b0-4e92-b59f-32c360823a9b",
	"内蒙古": "7c4e15a2-d078-4bc8-a749-1d8da697289c",
	"辽宁": "26fa2cd7-f876-48f2-b77b-8997f72d69b1",
	"吉林": "2d3b2de7-ba92-4715-955b-acd84bfe5a3c",
	"黑龙江": "b69c26d2-6531-4ef0-b9f1-748d52001616",
	"上海": "c628a2f2-04f8-4a00-b026-61a5381cbb8a",
	"江苏": "7d7126ab-cbda-43a2-bd4a-990291b20a4e",
	"浙江": "12407e48-3c80-46db-b3e2-fe396b1a4c05",
	"安徽": "33f722f0-1458-476b-af64-45f8722c42af",
	"福建": "54369554-a2f9-43e5-b0b4-7ac634cfe19d",
	"江西": "ea1645da-a1cb-48f2-9e6f-88b78fd1bb4e",
	"山东": "6528c818-024a-4ffe-9b9b-b3b8f04639a8",
	"河南": "aa89f644-1c7d-43c5-ad89-755b211adf05",
	"湖北": "d38721cc-5ece-4ac8-afc9-c7011f9ee3fc",
	"湖南": "9dc3d7ab-057e-4e19-9f21-f0b82874831c",
	"广东": "31b25d9c-912d-4db9-82ab-10d87a2885b3",
	"海南": "53d13c84-eec6-43db-8970-97a34ff60660",
	"重庆": "9577ea78-273e-4548-894b-bb239fbc8808",
	"四川": "a14280a0-b6bf-4495-87b4-9f74da8cf0a2",
	"贵州": "c23fc457-6ebe-4c26-8640-2d22c167297b",
	"云南": "6b02f013-2edd-4ac4-843a-377dada8316b",
	"西藏": "2e261e2c-5b1d-407f-8524-c77898fde3b9",
	"陕西": "3d3241ae-dbf4-4dae-adec-b96b33dc25e1",
	"甘肃": "480880d5-7574-4d47-927c-ae11b059827e",
	"青海": "9bd0c5e0-03e0-453b-a811-18e1c18c9431",
	"宁夏": "56e78036-b7d8-4c6c-9e81-174e1bd0d831",
	"新疆": "ada51f4f-1afe-4118-a32a-f51c3bb02d1e",
	"广西": "b6e1f2fe-fc64-493c-a683-cb1b8c99df4e",
	"台湾": "94dde1c1-98a8-4225-a058-fc65173ddf33"
}

second_step_param = {"__RequestVerificationToken": "",
                     "CompanyInfo.FromPage": "WebSite-Apply4",
                     "CompanyInfo.Name": "深圳有限公司",
                     "CompanyInfo.Type": choice(range(10)),
                     "CompanyInfo.Department": "电脑信息部",
                     "CompanyInfo.Position": "测试工程师",
                     "CompanyInfo.Income": 5000,
                     "CompanyInfo.EntryYear": 2015,
                     "CompanyInfo.EntryMonth": "2015-01",
                     "CompanyInfo.AreaCode": "0775",
                     "CompanyInfo.Phone": 86868787,
                     "CompanyInfo.PhoneExtension": "",
                     "CompanyInfo.ProvinceId": "",
                     "CompanyInfo.CityId": "",
                     "CompanyInfo.AreaId": "",
                     "CompanyInfo.Address": "车公庙"}

third_step_param = {"__RequestVerificationToken": "",
                    "ContactInfo.FromPage": "WebSite-Apply4",
                    "ContactInfo.RelativesName": "",
                    "ContactInfo.RelativesRelation": "兄弟",
                    "ContactInfo.RelativesPhone": "",
                    "ContactInfo.RelativesCompanyName": "深圳有限公司",
                    "ContactInfo.RelativesProvinceId": "",
                    "ContactInfo.RelativesCityId": "",
                    "ContactInfo.RelativesAreaId": "",
                    "ContactInfo.RelativesAddress": "车公庙",
                    "ContactInfo.ColleagueName": "",
                    "ContactInfo.ColleaguePosition": "测试",
                    "ContactInfo.ColleaguePhone": "",
                    "ContactInfo.OtherRelativesName": "",
                    "ContactInfo.OtherRelativesRelation": "远亲",
                    "ContactInfo.OtherRelativesPhone": "",
                    "IsAcceptPact": "True"
                    }

upload_param = {
	"Content-Disposition: form-data; name='Filename'": "02.jpg",
	"Content-Disposition: form-data; name='code'": "1.1",
	"Content-Disposition: form-data; name='ASPSESSIONID'": "kkpkghlk1uteybanh3gtlibx",
	"Content-Disposition: form-data; name='Filedata'; filename='%s'": "<file>",
	"Content-Type: application/octet-stream": "<file>",
	"Content-Disposition: form-data; name='Upload'": "Submit Query"
}

upload_file_code = {
	"身份证正面": "1.1",
	"身份证反面": "1.1",
	"授权委托书": "1.3",
	"近四个月流水": "1.2",
	"个人生活照": "1.4"
}
