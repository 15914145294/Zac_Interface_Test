# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     logUtil
   Description :
   Author :       Administrator
   date：          2018/8/18 0018
-------------------------------------------------
"""
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

from configs.config import *
from utils.constants import *

"""
log的工具类，用于输出和保存log
"""


class Logger(object):
	def __init__(self, logger_name="auto_interface"):
		print("---------Logger_init-------")
		# 初始化log
		self.logger = logging.getLogger(logger_name)
		# 设置根log的级别
		logging.root.setLevel(logging.NOTSET)

		log_cf = Config().get("log")
		# 保存log的文件名
		self.log_file_name = log_cf.get("file_name") if log_cf and log_cf.get("file_name") else "test.log"
		# 备份log的最大数量
		self.backup_count = log_cf.get("backup") if log_cf and log_cf.get("backup") else 100
		# 输出log的级别
		self.console_output_level = log_cf.get("console_level") if log_cf and log_cf.get("console_level") else 'INFO'
		# 保存到文件的log级别
		self.file_output_level = log_cf.get("file_level") if log_cf and log_cf.get("file_level") else 'DEBUG'
		# 日志输出格式 (时间 - log级别 - log名 - log)
		pattern = log_cf.get("pattern") if log_cf and log_cf.get(
			"pattern") else '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
		self.formatter = logging.Formatter(pattern)

	def get_logger(self):
		"""
		在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
			   我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
			   两个句柄的日志级别不同，在配置文件中可设置。
		"""
		if not self.logger.handlers:  # 避免重复日志
			console_handler = logging.StreamHandler()
			console_handler.setFormatter(self.formatter)
			console_handler.setLevel(self.console_output_level)
			self.logger.addHandler(console_handler)
			# 每天重新创建一个日志文件，最多保留backup_count份
			file_handler = TimedRotatingFileHandler(
				filename=os.path.join(LOG_PATH, time_tag + self.log_file_name),
				when='M',
				interval=1,
				backupCount=self.backup_count,
				delay=True,
				encoding='utf-8'
			)
			file_handler.setFormatter(self.formatter)
			file_handler.setLevel(self.file_output_level)
			self.logger.addHandler(file_handler)
		return self.logger


logger = Logger().get_logger()
