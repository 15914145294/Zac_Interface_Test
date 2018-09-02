# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       Administrator
   date：          2018/9/2 0002
-------------------------------------------------
"""
from random import choice
s = [{'Key': '广州市', 'Value': 'c1795c20-32fb-4b67-ae76-c6aab6e24a43'},
     {'Key': '韶关市', 'Value': '68682084-99f0-4b75-b6c8-218366d00ba9'},
     {'Key': '深圳市', 'Value': '92ce2049-36bf-4ae6-b831-22359c38f337'},
     {'Key': '珠海市', 'Value': 'b0c81c7f-eaec-40e6-ad6a-1dd0297fedb0'},
     {'Key': '汕头市', 'Value': '8b7c29eb-713f-4437-8d8d-e89324852ea5'},
     {'Key': '佛山市', 'Value': '706c2943-5675-4309-962b-0a0724c1856b'},
     {'Key': '江门市', 'Value': '359cefc2-c5ea-4e2e-a5be-d079345e72be'},
     {'Key': '湛江市', 'Value': '0eef16a8-6946-42f1-877a-447a2ad83818'},
     {'Key': '茂名市', 'Value': '46928154-02d7-4f2c-8112-02494a33aaf5'},
     {'Key': '肇庆市', 'Value': '9a534a06-8930-42f0-aa79-5ac679a6b2d4'},
     {'Key': '惠州市', 'Value': '4fa52a1b-7646-486d-89f3-44f1ac995cc3'},
     {'Key': '梅州市', 'Value': '6ae534ad-bca9-4efa-a73e-0792608bb2ff'},
     {'Key': '汕尾市', 'Value': 'e4b1e594-9d12-401c-927b-b820ae420063'},
     {'Key': '河源市', 'Value': '882b703d-a301-4281-9060-bf42ea443b85'},
     {'Key': '阳江市', 'Value': 'c5500ef4-1b35-4b5c-90fb-d78886c787b0'},
     {'Key': '清远市', 'Value': '81d54793-003b-43e5-ad49-2d8690308da9'},
     {'Key': '东莞市', 'Value': '7d6035d9-a842-4a8f-8efc-63a0d25b40ce'},
     {'Key': '中山市', 'Value': '82831d60-b3ed-4c43-a355-06e609c41e24'},
     {'Key': '潮州市', 'Value': 'a6a7bd21-203e-42c5-818d-c972abd15056'},
     {'Key': '揭阳市', 'Value': '1974e37b-48c6-4a12-89ad-567586b98700'},
     {'Key': '云浮市', 'Value': 'ce32b423-5025-4222-9923-77944fcb9156'}]
y = choice(s)["Value"]
print(y)