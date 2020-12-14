#!/usr/bin/env python
# coding=utf-8
# usage:
# obj3 = bakupOnePinnPatient(headInfo, patient_file)
# print obj3.getTarPackage()
import os
import re
import random
from readPatientInfo import readPatientInfo
#from Pinnutil.scan_standard_pinn_DB import scan_standard_pinn_DB
DEBUG = 0
MKDIR = '/usr/bin/mkdir'
TAR = '/usr/bin/tar'
COPY = '/usr/bin/cp'
GZIP = '/usr/bin/gzip'
MOVE = '/usr/bin/mv'
DELETE = '/usr/bin/rm'

tempHead = '''
InstitutionID = 721;
InstitutionPath = "Institution_721";
PinnInstitutionPath = "Institution_721";
Name = "---V92---Thorax";
StreetAddress = "";
StreetAddress2 = "";
City = "";
State = "";
ZipCode = "";
Country = "";
PatientLiteList ={
  PatientLite ={
    PatientID = 16780;
    PatientPath = "Institution_721/Mount_0/Patient_16780";
    MountPoint = "Mount_0";
    FormattedDescription = "Liu&&Xiumei-fusion&&&&358910&&ZhaoLujun&&2014-05-19 11:49:03";
    DirSize = 320.611;
  };
};
MountPointList ={
  SimpleString ={
    String = "Mount_0";
  };
};
SelectedMachineDirList ={
};
BackupMachineList ={
  BackupMachine ={
    Name = "(old) Varian 600CD,   ";
    Directory = "Machine.0";
    DirSize = 6.50879;
    WriteDate = "2010-02-06 15:11:34\";";
  };
  BackupMachine ={
    Name = "(old) 1304,   ";
    Directory = "Machine.1";
    DirSize = 3.64844;
    WriteDate = "2013-06-27 10:54:12\";";
  };
  BackupMachine ={
    Name = "Varian 600CD,   ";
    Directory = "Machine.10";
    DirSize = 6.50879;
    WriteDate = "2013-10-11 13:43:20\";";
  };
  BackupMachine ={
    Name = "(old) 5569,   ";
    Directory = "Machine.2";
    DirSize = 8.20996;
    WriteDate = "2013-06-27 11:05:52\";";
  };
  BackupMachine ={
    Name = "(old) Varian 600CD,   ";
    Directory = "Machine.3";
    DirSize = 6.50879;
    WriteDate = "2013-06-27 11:20:02\";";
  };
  BackupMachine ={
    Name = "(old) 1304,   ";
    Directory = "Machine.4";
    DirSize = 3.64844;
    WriteDate = "2013-06-26 11:32:39\";";
  };
  BackupMachine ={
    Name = "(old) 5569,   ";
    Directory = "Machine.5";
    DirSize = 8.08496;
    WriteDate = "2013-06-27 10:11:28\";";
  };
  BackupMachine ={
    Name = "(old) 1304_NEW,   ";
    Directory = "Machine.6";
    DirSize = 3.64844;
    WriteDate = "2013-09-14 10:20:49\";";
  };
  BackupMachine ={
    Name = "5569,   ";
    Directory = "Machine.7";
    DirSize = 8.20996;
    WriteDate = "2013-09-15 10:12:03\";";
  };
  BackupMachine ={
    Name = "1304,   ";
    Directory = "Machine.8";
    DirSize = 3.64844;
    WriteDate = "2013-09-14 11:15:57\";";
  };
  BackupMachine ={
    Name = "(old) 5569,   ";
    Directory = "Machine.9";
    DirSize = 8.20996;
    WriteDate = "2013-09-14 14:48:21\";";
  };
};
BackupMachineListNonCommissioned ={
  BackupMachine ={
    Name = "Varian 600CD,   ";
    Directory = "Machine.0";
    DirSize = 6.50879;
    WriteDate = "2014-02-07 15:17:21\";";
  };
  BackupMachine ={
    Name = "5569,   ";
    Directory = "Machine.1";
    DirSize = 8.20996;
    WriteDate = "2014-02-07 15:17:21\";";
  };
  BackupMachine ={
    Name = "1304,   ";
    Directory = "Machine.2";
    DirSize = 3.64844;
    WriteDate = "2014-02-07 15:17:21\";";
  };
};
BackupIsotopeList ={
};
BackupIsotopeListNonCommissioned ={
};
DeviceSpaceRequiredPatients = 0;
DeviceSpaceRequiredPhysics = 0;
DeviceSpaceRequiredScripts = 0;
DeviceSpaceRequiredOrganModels = 0;
DeviceSpaceRequiredAtlas = 0;
DefaultMountPoint = "Mount_0";
BackupDescription = "";
BackupVolume = "";
BackupFileName = "";
Session = "1";
ScriptsDir = "";
OrganModelsDir = "";
AtlasFile = "";
BackupTimeStamp = "";
BackupDeviceType = "None";
IsPatientBackup = 1;
IsPhysicsMachinesBackup = 0;
IncludePhysicsData = 0;
MachinesInV7Format = 0;
IsSolarisFormat = 1;
IncludeAllPatients = 0;
FullFileNameIncluded = 0;
BackupID = 0;
SortFields = "Patient Lastname";
ObjectVersion ={
  WriteVersion = "Launch Pad: 9.8";
  CreateVersion = "Launch Pad: 9.6";
  LoginName = "ww";
  CreateTimeStamp = "2014-05-27 10:08:47";
  WriteTimeStamp = "2014-07-01 15:56:18";
  LastModifiedTimeStamp = "2014-07-01.15:56:18";
};
DynamicRebuild = 0;
'''

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
            self.tarPackageObj = self.createTarFile(patientInfo, patHeadInfo)

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
        tarFile = patient_info['MedicalRecordNumber'] + '_' + patient_info['PatientID'] + '_' + patient_info['LastName'] + patient_info['FirstName'] + '_' + patient_info['MiddleName'] + '.tar'

        tarName = ''.join(tarFile.split())
        tarName = re.sub('`', '', tarName)
        tar_file_absPath = os.path.join(current_header_path, tarName)

        # Step1: tar header_file --'Institution'
        command = TAR + ' -c ' + ' --format=gnu ' + \
            ' -f ' + tar_file_absPath + ' Institution '
        print('  Tar File:%s', tarName)
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

        tarName = tarName + '.gz'
        tar_gzip_file_absPath = os.path.join(current_header_path, tarName)
        if not os.path.isfile(tar_gzip_file_absPath):
            os.system(command)
        os.chdir(path_backup)
        return tar_gzip_file_absPath


if __name__ == "__main__":
    work_path = "/home/pyang/bin/data/"
    headInfo = os.path.join(work_path, 'institution')
    patient_file = os.path.join(work_path, "Patient_3661")
    obj3 = bakupOnePinnPatient(headInfo, patient_file)
    print(obj3.createTarPackage())
    print("finish") 
