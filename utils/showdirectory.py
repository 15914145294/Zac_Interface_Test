# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     showdirectory
   Description :   展示文件内容
   Author :       Administrator
   date：          2018/9/16 0016
-------------------------------------------------
"""
import argparse
from pathlib import Path
from datetime import datetime


def convert_mode(mode: int):
	ret = ""
	modelist = ['r', 'w', 'x', 'r', 'w', 'x', 'r', 'w', 'x']
	modestr = bin(mode)[-9:]
	for i, c in enumerate(modestr):
		if c == "1":
			ret += modelist[i]
		else:
			ret += "-"
	return ret


def convert_type(file: Path):
	if file.is_symlink():
		return "l"
	elif file.is_dir():
		return "d"
	elif file.is_socket():
		return "s"
	elif file.is_fifo():
		return "p"
	else:
		return "-"


def human_size(size: int):
	units = ["B", "K", "M", "G", "T"]
	depth = 0
	while size >= 1024:
		size = size // 1024
		depth += 1
	return "{}{}".format(size, units[depth])


def show_dir(path, all=False, detail=False, human=False):
	p = Path(path)
	for file in p.iterdir():
		# .开头不打印 --all
		if not all and not str(file.name).startswith("."):
			continue
		# -l
		if detail:
			st = file.stat()
			size = st.st_size
			if human:
				size = human_size(size)
			yield [convert_type(file) + convert_mode(st.st_mode), st.st_nlink, st.st_uid, st.st_gid, str(size),
			       datetime.fromtimestamp(st.st_ctime).strftime("%Y-%m-%d %H:%M:%S"), file.name]
		else:
			yield file.name


parser = argparse.ArgumentParser(prog="ls", add_help=False, description="list all files")
parser.add_argument("path", nargs="?", default=".", help="path help")
parser.add_argument("-h", action="store_true")
parser.add_argument("-l", action="store_true")
parser.add_argument("-a", "--all", action="store_true")

if __name__ == '__main__':
	args = parser.parse_args("-l --all -h".split())
	# print(dir(args))
	for i in show_dir(args.path, args.l, args.all,args.h):
		print(i)
