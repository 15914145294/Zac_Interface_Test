# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       Administrator
   date：          2018/9/1 0001
-------------------------------------------------
"""

import unittest

from configs.config import *
from utils.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.constants import time_tag
from utils.fileutil import CommonMethods
from utils.logUtil import logger

if __name__ == '__main__':
	logger.info("-" * 40 + "测试开始" + "-" * 40)
	report = REPORT_PATH + '\\report_%s.html' % time_tag
	suite = unittest.TestSuite()
	# case_home = unittest.TestLoader().loadTestsFromTestCase(CaseHome)
	# case_menu = unittest.TestLoader().loadTestsFromTestCase(CaseMenu)
	# tests = [case_home, case_menu]
	discover = unittest.defaultTestLoader.discover(CASE_PATH, pattern='test_*.py')
	suite.addTests(discover)
	with open(report, 'wb+') as f:
		runner = HTMLTestRunner(stream=f, verbosity=2, title='自动化接口测试',
		                        description=''
		                        )
		runner.run(suite)
	logger.info("-" * 40 + "测试结束" + "-" * 40)
	logger.info("-" * 40 + "发送邮件" + "-" * 40)
	mail_cf = Config().get("mail")
	log_path = os.path.join(LOG_PATH, "%stest.log" % time_tag)
	accessory_list = [log_path, report]

	report_html = CommonMethods.read_file(report)
	# e = Email(title='接口测试报告',
	#           receiver=mail_cf.get("EMAIL_RECEIVER"),
	#           server=mail_cf.get("EMAIL_SERVER"),
	#           sender=mail_cf.get("EMAIL_SENDER"),
	#           password=mail_cf.get("EMAIL_PASSWORD"),
	#           message=report_html,
	#           path=accessory_list
	#           )
	# e.send()
