#!/usr/bin/env python
# coding=utf-8
# usage:
# obj3 = bakupOnePinnPatient(headInfo, patient_file)
# print obj3.getTarPackage()
import os
import re
import glob
import shutil
from bakupOnePinnPatient import bakupOnePinnPatient

def bakOneInst(instPath,exportPath):
    if not os.path.isdir(exportPath):
        os.mkdir(exportPath)

    instName = os.path.abspath(instPath)
    if 'Institution_' in instName:
        planPoolPath = os.path.join(instPath,'Mount_0')
    else:
        planPoolPath = instPath
    os.chdir(planPoolPath)
    plans = glob.glob('Patient_*')
    if len(plans) == 0:
        print('Not valid Pinancle Data')
    else:
        print('Total%d Plans:'%len(plans))
        for ind, dir in enumerate(plans):
            print("Total:%d,Current:%d"%(len(plans),ind))
            obj3 = bakupOnePinnPatient(headInfo, os.path.join(planPoolPath, dir))
            tarPack = obj3.createTarPackage()
            if tarPack:
                try:
                    shutil.move(tarPack,os.path.join(exportPath,os.path.basename(tarPack)))
                except Exception as e:
                    exit()
        print('BakupAllPat!')


if __name__ == "__main__":
    workPath = "/home/p3rtp/bin/bakup/"    
    headInfo = os.path.join(workPath, 'institution')
    # exportPath = os.path.join(workPath, 'export')
    exportPath = '/mnt/bak/bakup/temp'
    instPath   = '/pinnacle_patient_expansion/NewPatients/Institution_3364'

    bakOneInst(instPath, exportPath)

