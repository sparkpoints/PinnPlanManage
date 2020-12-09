#!/usr/bin/env python
# coding=utf-8
# usage:
# obj3 = bakupOnePinnPatient(headInfo, patient_file)
# print obj3.getTarPackage()
import os
import re
import random
from ../Pinnutil.readPatientInfo import readPatientInfo
#from Pinnutil.scan_standard_pinn_DB import scan_standard_pinn_DB
DEBUG = 0
MKDIR = '/bin/mkdir'
TAR = '/bin/tar'
COPY = '/bin/cp'
GZIP = '/bin/gzip'
MOVE = '/bin/mv'
DELETE = '/bin/rm'


class bakupOnePinnPatient(object):
    def __init__(self, headInfo=None, targetDir=None):
        self.tarPackageObj = None
        self.headInfo = headInfo
        self.targetDir = targetDir

        if not os.path.isdir(targetDir):
            print("ERROR: %s is not exist\n" % targetDir)



    def createTarPackage(self):
        # if not self.targetDir:
        patientInfo = self.getPatientBasicInfo(self.targetDir)
        if patientInfo:
            patHeadInfo = self.createPatientHeaderInfo(headInfo, patientInfo)
        if patHeadInfo:
            self.tarPackageObj = self.create_tar_file(
                    patientInfo, patHeadInfo, targetDir)

    def createPatientHeaderInfo(self, headInfo, patient_info_object):
        source_file = headInfo
        base_dir = os.path.split(source_file)[0]
        sourceObj = open(source_file, 'r')

        target_file = os.path.join(base_dir, 'Institution')
        headerObj = open(target_file, 'w+')

        patientData = patient_info_object.get_patient_data()
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

    def getPatientBasicInfo(self, data_dir):
        # data_dir is the abs path to patient dir
        patient_obj = None
        if os.path.isdir(data_dir) and os.path.isfile(os.path.join(data_dir, 'Patient')):
            patient_obj = readPatientinfo(os.path.join(data_dir, 'Patient'))
        if patient_obj is None:
            print("%s is not a validate pinnalce3 TPS patient Dir\n" % data_dir)
            return None
        else:
            return patient_obj

    def getTarPackage(self):
        return self.tarPackageObj

    def create_tar_file(self, patient_info_object, patHeadInfo, data_dir):
        path_backup = os.getcwd()
        current_header_path = os.path.split(patHeadInfo)[0]
        os.chdir(current_header_path)

        patient_info = patient_info_object.get_patient_data()
        tarFile = patient_info['PatientID'] + '_' + patient_info['MedicalRecordNumber'] + '_' + patient_info['LastName'] + patient_info[
            'FirstName'] + '_' + patient_info['MiddleName'] + '.tar'

        tarName = ''.join(tarFile.split())
        tarName = re.sub('`', '', tarName)
        tar_file_absPath = os.path.join(current_header_path, tarName)

        # Step1: tar header_file --'Institution'
        command = TAR + ' -c ' + ' --format=gnu ' + \
            ' -f ' + tar_file_absPath + ' Institution '
        print '  Tar File:', tarName
        if not DEBUG:
            os.system(command)

        # Step2: tar Patient Content directory "Institution_XXX/Mount_0/Patient_XXXX"
        patient_data_path = os.path.split(data_dir)[0]
        patient_data_dir = os.path.split(data_dir)[1]
        os.chdir(patient_data_path)

        command = TAR + ' -r ' + ' --format=gnu ' + ' -f ' + \
            tar_file_absPath + ' ' + patient_data_dir
        if not DEBUG:
            os.system(command)

        # Step3: compress tar file using gzip
        os.chdir(current_header_path)
        command = GZIP + ' ' + tarName
        #
        # if not DEBUG:
        #     os.system(command)

        tarName = tarName + '.gz'
        tar_gzip_file_absPath = os.path.join(current_header_path, tarName)
        if not os.path.isfile(tar_gzip_file_absPath):
            os.system(command)
        os.chdir(path_backup)
        return tar_gzip_file_absPath


if __name__ == "__main__":
    work_path = "/home/peter/PinnWork"
    headInfo = os.path.join(work_path, 'institution_template')
    patient_file = os.path.join(work_path, "Patient_30530")
    obj3 = bakupOnePinnPatient(headInfo, patient_file)
    print(obj3.getTarPackage())
    print("finish") 
