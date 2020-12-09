#! /usr/bin/env python
# coding=utf-8
# 
import os
import re
import logging

def cleanPinnOriData(poolpath):
    """[clean 2 type temp files]
        1. links to files 
        2. autosave files
    Args:
        poolpath ([string]): [home dir of path]
    """

    MatchRegList = ['^.auto.plan*',
                    '.ErrorLog$',
                    '.Transcript$',
                    '.defaults$',
                    '.pinnbackup$',
                    '^Institution.\d+',
                    '^Patient.\d+',
                    '\s*~\s*',
                    '.json$']

    for dirpath, dirname, filenames in os.walk(poolpath):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            #type1:links file check
            if os.path.islink(filepath):
                os.remove(filepath)
                continue
            #type2:autosave files
            for currentReg in MatchRegList:
                if re.findall(currentReg, file):
                    os.remove(filepath)
                    print('del:%s\n' % filepath)
        if dirname:
            for currendir in dirname:
                cleanPinnOriData(os.path.join(dirpath,currendir))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='cleanPinnOriData.log',
                    filemode='w')
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    work_path = '/home/peter/PinnWork/'
    os.chdir(work_path)
    targetpath = os.path.join(work_path, 'Mount_Lung12')
    if os.path.isdir(targetpath):
        cleanPinnOriData(targetpath)
        logging.info('cleanPinnOriData success')
    else:
        logging.debug("not fined %s", targetpath)
