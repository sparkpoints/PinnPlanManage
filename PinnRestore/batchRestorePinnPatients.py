#! /usr/bin/env python
# coding=utf-8
# 2010-2017.12 all Patients tars in one place
# this scripts used to batch find and restore to remote server1(10.36.126.101)
import os
import sys
# sys.path.append('./Pinnutil')
import logging
# import FTPModule
import shutil

import numpy as np
import pandas as pd
import pypinyin


PINN_TRA_PATH = '/mnt/g/Pinn2020/'
WORKING_PATH = '/home/pyang/PinnWork/'
LOCAL_DIR_PATH = os.path.join(WORKING_PATH, 'export')
WANTED_LIST = os.path.join(WORKING_PATH, 'WantedList.CSV')

EXPORT_PATH = '/mnt/g/export/'

FTP_IP = '172.31.28.202'
FTP_USER = 'p3rtp'
FTP_PASSWD = 'p3rtp123'
FTP_REMOTE_PATH = '/home/p3rtp/PinnRestoreDir'


def RetorePinnPatients(localDirPath, wantedFile, targetDirPath, loggerHand, ftpMode=True,):
    wantedList = []
    # if ftpMode:
    #     ftpHandle = FTPModule.ftpExt(FTP_IP)
    #     ftpHandle.Login(FTP_USER, FTP_PASSWD)
    #     targetDirPath = os.path.basename(FTP_REMOTE_PATH)
    #     ftpHandle.changePath(targetDirPath)
    try:
        fileHand = open(wantedFile, 'r')
        for mrn in fileHand.readlines():
            wantedList.append(mrn.strip())
    except IOError:
        raise
    localFileList = os.listdir(localDirPath)
    ind = 1
    for tarFile in localFileList:
        curMRN = tarFile.split('_')[1]
        if curMRN in wantedList:
            loggerHand.info(tarFile)
            shutil.copyfile(os.path.join(PINN_TRA_PATH, tarFile),
                            os.path.join(EXPORT_PATH, tarFile))
            # if ftpHandle and not ftpHandle.isExist(tarFile, '.'):
            #     #print("upload file %s", ind, tarFile)
            #     loggerHand.info("uploadFile(%d of %d):%s",
            #                     (ind, len(wantedList), tarFile))
            #     ind += 1
            #     ftpHandle.UpLoadFile(os.path.join(
            #         localDirPath, tarFile), tarFile)

# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

def restPatBatch(restListFile,oriDataPool,exportDir,logger):
    try:
        df = pd.read_csv(restListFile, encoding='gbk')
    except IOError:
        raise "No such file%s"%restListFile
    
    mrnList = []
    nameList = []
    if 'Name' in df.columns:
        # nameList = df['Name']
        for name in df['Name']:
            strName = pinyin(name)
            # logger.info(strName)
            nameList.append(strName)

    if 'MRN' in df.columns:
        mrnList = df['MRN']
    logger.info(len(mrnList))
    findFiles = []
    noFindF = []


    # targetList = []
    for root, dirs, files in os.walk(oriDataPool):
        # targetList = files   
        logger.info(len(files))
        if len(mrnList) == len(nameList):
            for mrn, name in zip(mrnList, nameList):
                findMark = 0
                for file in files:
                    mrnStr = '_' + str(mrn) + '_'
                    nameStr = '_' + str(name) + '_'
                    combStr = '_' + str(mrn) + '_' + str(name) + '_'
                    if combStr in file.lower():
                        findMark = 1
                        findFiles.append(os.path.join(root,file))
                        shutil.copy(os.path.join(root, file),
                                    os.path.join(exportDir, file))
                        logger.info('Find:%s:%s:%s' % (mrn, name, file))
                        break
                    elif (mrnStr in file.lower()) or (nameStr in file.lower()):
                        findMark = 1
                        findFiles.append(file)
                        shutil.copy(os.path.join(root, file),
                                    os.path.join(exportDir, file))
                        logger.info('Find:%s:%s:%s' % (mrn, name,file))

                if not findMark:
                    noFindF.append(mrn)
                    logger.warning('NoSuch:%s:%s' % (mrn, name))

    

    
    
    # for file in findFiles:
    #     print(file)
    #     shutil.copy(file, os.path.join(exportDir,os.path.basename(file)))

    logger.info(len(findFiles))
    logger.warning(len(noFindF))


if __name__ == "__main__":
    logger = logging.getLogger('batch restoe pinnalce')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('begin!')
    # RetorePinnPatients(PINN_TRA_PATH, WANTED_LIST,
    #                    LOCAL_DIR_PATH, logger, False)
    restPatBatch(WANTED_LIST,PINN_TRA_PATH,EXPORT_PATH,logger)
