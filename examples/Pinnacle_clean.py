#! /usr/bin/env python
# coding=utf-8

import time
import os
import re
#import ftplib
from ftplib import FTP

import ParsePinnacleFile

def CleaningPatientPool(poolpath,matchRegs,logfile):
    for dirpath,dirname,filenames in os.walk(poolpath):
        for file in filenames:
            for currentReg in matchRegs:
                if re.findall(currentReg,file):
                    filepath = os.path.join(dirpath,file)
                    os.remove(filepath)
                    print ('del:%s\n' % filepath)
                    logfile.write('del:%s\n'%filepath)

def GetPatientPath(searchPath,PatientListFile,WantedFile,logobj):
    wantedList = []
    PatientList = open(PatientListFile, 'r').read().split('\n')
    Wantedobj      = open(WantedFile, 'r')

    for wantedPatient in Wantedobj.readlines():
        for PatientInfo in PatientList:
            patientInfoList = PatientInfo.split(',')
            wantedPatientList = wantedPatient.split(',')
            if re.match(wantedPatientList[0],patientInfoList[0]):
                path = os.path.join(searchPath,patientInfoList[3])
                logobj.write('%s,%s\n'%(patientInfoList[0],patientInfoList[3]))
                wantedList.append(path)
                print PatientInfo
    return wantedList

def FTP2Pinnacle(wantedList,targetdir):
    IP_Addr = '10.36.126.63'
    ftpUser = 'peter'
    ftpPass = 'whoami1'
    ftpPort = 21
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(IP_Addr,ftpPort)
    ftp.login(ftpUser,ftpPass)
    print ftp.getwelcome()
    # ftp.sendcmd()
    # ftp.cmd("xxx/xxx")  #进入远程目录
    # bufsize = 1024  # 设置的缓冲区大小
    # filename = "filename.txt"  # 需要下载的文件
    # file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
    # ftp.retrbinaly("RETR filename.txt", file_handle, bufsize)  # 接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)  # 关闭调试模式
    ftp.quit()  # 退出ftp
def compareTwoCSVfile(firstplus,secendplus,firstfile,secendfile,logobj):
    firstlist = open(firstfile, 'r').read().split('\n')
    seconlist = open(secendfile, 'r').read().split('\n')
    firstplusobj = open(firstplus,'w+')
    secendplusojb = open(secendplus,'w+')

    for line1 in firstlist:
        if line1 in seconlist:
            continue
        else:
            firstplusobj.write('%s\n'%line1)
    for line2 in seconlist:
        if line2 in firstlist:
            continue
        else:
            secendplusojb.write('%s\n'%line2)

    firstplusobj.close()
    secendplusojb.close()

if  __name__ == "__main__":
    #sourcepath = "/Volumes/PinnSETemp/NewPatients/"
    PinnPatientPool = '/Volumes/PinnSETemp/NewPatients/'
    basepath        = "/Users/yang/Downloads/ESO/"
    PatientsRecordListFile = os.path.join(basepath,'PinnaclePatientPools.csv')
    PatientWantedListFile  = os.path.join(basepath,'WantedList.csv')
    filename    = time.asctime() + '.csv'
    listfile    = os.path.join(basepath,filename)
    outobj      = open(listfile,'w+')

    MatchRegList = ['^.auto.pl4an*',\
                    '.ErrorLog$',\
                    '.Transcript$',\
                    '.defaults$',\
                    '.pinnbackup$',\
                    '^Institution.\d+',\
                    '\s*~\s*']
    CleaningPatientPool(basepath,MatchRegList,outobj)
    #FTP2Pinnacle('','')
    results = GetPatientPath(PinnPatientPool,PatientsRecordListFile,PatientWantedListFile,outobj)
    outobj.close()
    print "end"
