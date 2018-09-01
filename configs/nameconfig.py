# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     nameUtil
   Description :
   Author :       Administrator
   date：          2018/8/18 0018
-------------------------------------------------
"""
"""
A:将first_names列表转换成json字符串
B：将last_names列表转换成json字符串
C：创建文件句柄以供json.dump写入
D: json序列化两个列表并将其写入到文件中
"""
import json

last_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
              '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
              '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

first_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
               '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
               '乾', '坤']

res = json.dumps(first_names, ensure_ascii=False)
first_fb = open('first_names.json', 'w', encoding='utf8')
last_fb = open('last_names.json', 'w', encoding='utf8')

FIRSTNAME = json.dump(first_names, first_fb, ensure_ascii=False, indent=10)
LASTNAME = json.dump(last_names, last_fb, ensure_ascii=False, indent=10)
