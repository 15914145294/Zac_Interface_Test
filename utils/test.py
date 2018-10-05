# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       Administrator
   date：          2018/9/8 0008
-------------------------------------------------
"""
from requests.structures import CaseInsensitiveDict

cid = CaseInsensitiveDict()
cid['Accept'] = 'application/json'
print(cid['aCCEPT'] == 'application/json')  # True
print(list(cid) == ['Accept'])

