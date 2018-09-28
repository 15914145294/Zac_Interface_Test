# encoding:utf-8

from ftplib import FTP
import os
import sys
import time

_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'


class FtpClient(object):
    def __init__(self):
        self.ftp = None

    def __del__(self):
        pass

    def setFtpParams(self, ip, uname, pwd, port=21, timeout=60):
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout

    def initEnv(self):
        if self.ftp is None:
            self.ftp = FTP()
            print('### connect ftp server: %s ...' % self.ip)
            self.ftp.connect(self.ip, self.port, self.timeout)
            self.ftp.login(self.uname, self.pwd)
            print(self.ftp.getwelcome())
            self.ftp.set_pasv(False)

    def clearEnv(self):
        if self.ftp:
            self.ftp.close()
            print('### disconnect ftp server: %s!' % self.ip)
            self.ftp = None

    def uploadDir(self, localDir='./', remoteDir='./'):
        if not os.path.isdir(localDir):
            return
        self.ftp.cwd(remoteDir)
        for file in os.listdir(localDir):
            source = os.path.join(localDir, file)
            if os.path.isfile(source):
                self.uploadFile(source, file)
            elif os.path.isdir(source):
                try:
                    self.ftp.mkd(file)
                except:
                    sys.stderr.write('The dir is exists %s' % file)
                self.uploadDir(source, file)
        self.ftp.cwd('..')

    def uploadFile(self, localPath, remotePath='./'):

        if not os.path.isfile(localPath):
            return
        print(' upload %s to %s' % (localPath, remotePath))
        self.ftp.storbinary('STOR ' + remotePath, open(localPath, 'rb',encoding="utf-8"))

    def __filetype(self, src):
        if os.path.isfile(src):
            index = src.rfind('/')
            # if the src not contains /
            if index == -1:
                index = src.rfind('/')
            return _XFER_FILE, src[index + 1:]
        elif os.path.isdir(src):
            return _XFER_DIR, ''

    def upload(self, localDir="./", remoteDir="./"):
        time.sleep(20)
        filetype, filename = self.__filetype(localDir)

        self.initEnv()
        if filetype == _XFER_DIR:
            self.srcDir = localDir
            self.uploadDir(self.srcDir, remoteDir)
        elif filetype == _XFER_FILE:
            self.uploadFile(localDir, filename)
        self.clearEnv()

    def download_file(self, localfile, remotefile):

        self.debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % localfile)
        # return
        with open(localfile, 'wb') as f:
            self.ftp.retrbinary('RETR %s' % (remotefile), f.write)

    def download_files(self, localDir='./', remoteDir='./'):
        """
        从远程目录下，下载所有的文件并创建对应的目录
        :param localdir: 本地文件夹
        :param remotedir: 远程服务文件夹
        :return:
        """
        try:
            self.ftp.cwd(remoteDir)
            print(self.ftp.pwd())
        except:
            self.debug_print(u'目录%s不存在，继续...' % remoteDir)
            return
        if not os.path.isdir(localDir):
            os.makedirs(localDir)
        self.debug_print(u'切换至目录 %s' % self.ftp.pwd())
        self.file_list = []
        #
        # self.ftp.dir(self,*args) List a directory in long form
        # 最后一个参数为回调函数，前面的不为空的参数，会跟list 组合成command
        # 默认列出当前目录下的内容
        #
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list
        # print(remotenames)
        # return
        for item in remotenames:
            filetype = item[0]
            filename = item[1]
            local = os.path.join(localDir, filename)
            if filetype == 'd':
                self.download_files(local, filename)
            elif filetype == '-':
                self.download_file(local, filename)
        self.ftp.cwd('..')
        self.debug_print('返回上层目录 %s' % self.ftp.pwd())

    def get_file_list(self, line):
        """

        :param lines: ftp.dir() provide the line
        :return: return the file list ,that get file name from line
        """
        # ret_arr = []
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def debug_print(self, s):
        print(s)

    def get_filename(self, line):
        """
        line maybe :-rw-r--r--    1 501      501        320294 Aug 24 05:08 1.d2dc00a98a6eee589f2e.chunk.js
        :param line:
        :return: return the first word of line and get the file name.
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr


if __name__ == '__main__':
    xfer = FtpClient()
    xfer.setFtpParams(sys.argv[1], sys.argv[2], sys.argv[3])
    xfer.initEnv()
    xfer.upload(localDir=sys.argv[4], remoteDir=sys.argv[5])
