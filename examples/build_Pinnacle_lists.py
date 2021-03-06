#! /usr/bin/env python
# coding=utf-8
#Pinnacle3 TPS的病例数据由2部分数据组成，1：Patient_XXX，2：MRN_Name.tar.gz
#通过此程序编列所有的病例，构建一个log文件（列表），记录所有病人
#列表文件内容：每一行为一个病例，
#文件内容是：

import time
import os
import re
import tarfile



import ParsePinnacleFile

#built whole poole,iter into each instituion(group)
def Build_whole_Patient_Pool(poolpath,PatientList,logfile):
    for institution in os.listdir(poolpath):
        if re.match('Institution_\d+',institution) and os.path.isdir(os.path.join(poolpath,institution)):
            localpath = os.path.join(poolpath,institution,'Mount_0')
            Build_single_Institution(localpath,PatientList,logfile)

#build patients in Institution(group, head&Neck,thorax,abdomen)
def Build_single_Institution(path,PatientList,logfile):
    for curdir in os.listdir(path):
        if curdir == '.' or curdir == '..':
            continue
        elif re.match('Patient_\d+', curdir):
            currentfile = os.path.join(path, curdir, 'patient')
            if os.path.isfile(currentfile):
                data = ParsePinnacleFile.readsinglefile(open(currentfile))
                formattedPatientList(data,PatientList,logfile,None)

#formatter result into logfile
def formattedPatientList(data,PatientList,logfile,appendstr=None):
    if data is None:
        return None
    else:
        print "%s,%s%s" % (data['MedicalRecordNumber'], data['LastName'], data['FirstName'])
        # if data['PatientID'] in PatientIDList:
        #     return None
        if re.match('Patient_\d+', data['LastName']) and data['MedicalRecordNumber'] is None:
            return None
        elif data['LastName'] is None and data['FirstName'] is None and data['MedicalRecordNumber'] is None:
            return None
        else:
            if appendstr: #gzip file using tar_path for searching
                logfile.write("%s,%s%s,%s,%s,%s,%s\n" % (data['MedicalRecordNumber'], \
                                                         data['LastName'], \
                                                         data['FirstName'], \
                                                         data['PatientID'], \
                                                         appendstr, \
                                                         data['MiddleName'], \
                                                         data['CreateTimeStamp']))
            else: #native directory patient for searching
                logfile.write("%s,%s%s,%s,%s,%s,%s\n" % (data['MedicalRecordNumber'],\
                                                         data['LastName'], \
                                                         data['FirstName'], \
                                                         data['PatientID'], \
                                                         data['PatientPath'], \
                                                         data['MiddleName'], \
                                                         data['CreateTimeStamp']))
            PatientList.append(data['PatientID'])
            return (PatientList,logfile)

#some patients backup in tar and gz type files
def Build_tar_Patients(path,PatientList,logfile):
    for dirpath,dirnames,filenames in os.walk(path):
        for file in filenames:

            currentFile = os.path.join(dirpath,file)

            extension = os.path.splitext(currentFile)[1][1:]
            if not extension:
                continue
            elif extension == "tar" or extension == 'gz':
                if extension == "tar":
                    options = 'r:tar'
                elif extension == 'gz':
                    options = 'r:gz'
                tar = tarfile.open(currentFile,options)
                for member in tar.getmembers():
                    if re.findall('Patient$',member.name):
                        fobj = tar.extractfile(member)
                        data = ParsePinnacleFile.readsinglefile(fobj)
                        formattedPatientList(data, PatientList, logfile,currentFile)



if  __name__ == "__main__":

    #sourcepath = "/Volumes/PinnSETemp/NewPatients/"
    sourcepath = "/Users/yang/Downloads/ESO/"
    listfile   = "/Users/yang/Downloads/"+ "PinnaclePoolPatients" + time.asctime() + '.csv'
    outobj = open(listfile,'w+')
    PatientIDList = []
    #Build_whole_Patient_Pool(sourcepath,PatientIDList,outobj)
    #Build_single_Institution("/Volumes/PinnSETemp/NewPatients/Institution_3856/Mount_0", PatientIDList, outobj)
    Build_tar_Patients(sourcepath,PatientIDList,outobj)
    outobj.close()
    print "end"
