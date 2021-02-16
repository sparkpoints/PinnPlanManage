#!/usr/bin/env python
# coding=utf-8
# usage:
# obj3 = bakupOnePinnPatient(headInfo, patient_file)
# print obj3.getTarPackage()
import os
import re
import random
import shutil
import subprocess
from readPatientInfo import readPatientInfo
#from Pinnutil.scan_standard_pinn_DB import scan_standard_pinn_DB
"""
Solaris Shell tar cmd:
gnutar -c -h -f /home/p3rtp/aa.1.tar --exclude=.auto.plan.Trial.binary.* 
-C /usr/local/adacnew/Patients Institution 
-C /usr/local/adacnew/Patients Insitution_3194/Mount_0/Patient_41099 2>&1
"""



DEBUG = 0
MKDIR = '/usr/bin/mkdir'
TAR = '/usr/bin/gnutar'
COPY = '/usr/bin/cp'
GZIP = '/usr/bin/gzip'
MOVE = '/usr/bin/mv'
DELETE = '/usr/bin/rm'


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
                cleanPinnOriData(os.path.join(dirpath, currendir))

class bakupOnePinnPatient(object):
    def __init__(self, headInfo=None, targetDir=None):
        self.tarPackageObj = None
        self.headInfo = headInfo
        self.targetDir = targetDir
        if not os.path.isdir(targetDir):
            print("ERROR: %s is not exist\n" % targetDir)

    def createTarPackage(self):
        # if not self.targetDir:
        patientInfo = self.getPatientBasicInfo()
        patHeadInfo = None
        if patientInfo:
            patHeadInfo = self.createPatientHeaderInfo(patientInfo)
        if patHeadInfo:
           return self.createTarFile(patientInfo, patHeadInfo)
           

    def createPatientHeaderInfo(self, patInfoObj):
        source_file = self.headInfo
        base_dir = os.path.split(source_file)[0]
        sourceObj = open(source_file, 'r')

        target_file = os.path.join(base_dir, 'Institution')
        headerObj = open(target_file, 'w+')

        patientData = patInfoObj.getPatientData()
        PatientPath = patientData['PatientPath']
        inst_name = PatientPath.split('/')[0]
        inst_number = inst_name.split('_')[-1]
        formatted_str = patientData['LastName'] + '&&' \
            + patientData['FirstName'] + '&&' \
            + patientData['MedicalRecordNumber'] + '&&' \
            + patientData['RadiationOncologist'] + '&&' \
            + patientData['WriteTimeStamp']
        for line in sourceObj.readlines():
            if re.search('^InstitutionID*', line):
                headerObj.write("InstitutionID = %s;\n" % inst_number)
                continue
            elif re.search('^InstitutionPath*', line):
                headerObj.write("InstitutionPath = \"%s\";\n" % inst_name)
                continue
            elif re.search('^PinnInstitutionPath*', line):
                headerObj.write("PinnInsitutionPath = \"%s\";\n" % inst_name)
                continue
            elif re.search('^    PatientID*', line):
                headerObj.write('    ')
                headerObj.write("PatientID = %s;\n" % patientData['PatientID'])
                continue
            elif re.search('^    PatientPath*', line):
                headerObj.write('    ')
                headerObj.write("PatientPath = \"%s\";\n" %
                                patientData['PatientPath'])
                continue
            elif re.search('^    FormattedDescription*', line):
                headerObj.write('    ')
                headerObj.write(
                    "FormattedDescription = \"%s\";\n" % formatted_str)
                continue
            elif re.search('^    DirSize*', line):
                headerObj.write('    ')
                headerObj.write("DirSize = %s;\n" % patientData['DirSize'])
                continue
            else:
                headerObj.write(line)
        headerObj.close()
        return target_file

    def getPatientBasicInfo(self):
        # data_dir is the abs path to patient dir
        data_dir = self.targetDir
        patient_obj = None
        if os.path.isdir(data_dir) and os.path.isfile(os.path.join(data_dir, 'Patient')):
            patient_obj = readPatientInfo(os.path.join(data_dir, 'Patient'))
        if patient_obj is None:
            print("%s is not a validate pinnalce3 TPS patient Dir\n" % data_dir)
            return None
        else:
            return patient_obj

    def getTarPackage(self):
        return self.tarPackageObj

    def createTarFile(self, patInfoObj, patHeadInfo):
        data_dir = self.targetDir
        path_backup = os.getcwd()
        current_header_path = os.path.split(patHeadInfo)[0]
        os.chdir(current_header_path)

        patient_info = patInfoObj.getPatientData()
        tarName = patient_info['PatientID'] + '_' + \
            patient_info['MedicalRecordNumber'] + '_' + \
            patient_info['LastName'] + patient_info['FirstName'] + '_' + \
            patient_info['MiddleName'] + '_' + \
            str(random.randint(1, 1000)) + '.gtar'

        tarName = ''.join(tarName.split())
        tarName = re.sub('%', '', tarName)
        tarName = re.sub('#', '', tarName)
        tarName = re.sub('&', '', tarName)
        # tarName = re.sub('?', '', tarName)
        tarName = re.sub('`', '', tarName)

        tar_file_absPath = os.path.join(current_header_path, tarName)

        # Step1: tar header_file --'Institution'
        command = []
        command.append(TAR)
        command.append('-c')
        command.append('-z')
        command.append('-h')
        command.append('-f')
        command.append(tar_file_absPath)
        command.append('--exclude=.auto.plan.Trial.binary.*')
        command.append('-C')
        command.append(current_header_path)
        command.append('Institution')
        command.append('-C')
        command.append(os.path.dirname(data_dir))
        command.append(os.path.basename(data_dir))
       
        try:
            print("BAKUP:%s.........." % tarName)
            subprocess.call(command)
            return tar_file_absPath
            # print("Sucess!\n")
        except Exception as e:
            print("BAKUP:%s.....Failed\n" % tarName)



if __name__ == "__main__":
    work_path = "/home/p3rtp/bin/bakup/"
    headInfo = os.path.join(work_path, 'institution')
    patient_file = os.path.join(work_path, 'Mount_0', "Patient_35436")
    obj3 = bakupOnePinnPatient(headInfo, patient_file)
    obj3.createTarPackage()
    print("finish") 
