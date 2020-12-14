#!/usr/bin/env python
# coding=utf-8
# usage:
# obj3 = bakupOnePinnPatient(headInfo, patient_file)
# print obj3.getTarPackage()
import os
import re
from bakupOnePinnPatient import bakupOnePinnPatient

if __name__ == "__main__":
    workPath = "/home/pyang/bin/data/"
    instPath = '/mnt/d/PinnData'
    headInfo = os.path.join(workPath, 'institution')
    # patient_file = os.path.join(work_path, "Patient_3661")
    for dir in os.listdir(instPath):
        print(os.path.join(instPath, dir))
        obj3 = bakupOnePinnPatient(headInfo, os.path.join(instPath, dir))    
        print(obj3.createTarPackage())
