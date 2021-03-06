#! /usr/bin/env python
# coding=utf-8
# input: file "/home/peter/Patient_6527/Patient"
# output：a dict = obj.getPatientData
import os
import re
import io
class readPatientInfo(object):
    '''parse simple pinnacle TPS raw data file,
    like:"patient" text format file
    return a dict object:dict[var_name] = value'''

    def __init__(self, filePath):
        self.file = filePath
        self.patientData = None

        if os.path.isfile(self.file):
            # self.fileObj = open(self.file,'r', encoding='utf-8')
            with io.open(self.file, 'r', encoding='unicode_escape') as f:
                self.patientData = self.readSinglefile(f)
                # self.fileObj.close()

    def getPatientData(self):
        return self.patientData

    def readSinglefile(self, fileObj):
        PatientData = {}
        if fileObj:
            for line in fileObj.readlines():
                if not re.search('\=', line):
                    '''only parse line in style "var_name = value;",
                    escape all other lines'''
                    continue
                elif re.search('CreateTimeStamp', line):
                    continue
                elif re.search('^DirSize*', line):
                    '''sub_function exit port
                    DirSize is the final line of Pinn Patient file'''
                    (key, value) = self.readSingleValue(line)
                    PatientData[key] = value
                    return PatientData
                elif re.search('^  CreateTimeStamp*', line):
                    '''there many createTimestamp,only record this line'''
                    (key, value) = self.readSingleValue(line)
                    PatientData[key] = value
                else:
                    (key, value) = self.readSingleValue(line)
                    PatientData[key] = value

    def readSingleValue(self, str):
        ''' parse one line "var_name = value;",
        return (var_name, value)'''
        str = str.strip()
        if re.search('\;', str):
            str = str[0:-1]
        str = str.replace("\"", '')
        data = str.split('=')
        return (data[0].strip(), data[1].strip())


if __name__ == "__main__":
    patientfile = "/home/pyang/bin/data/Patient_3661/Patient"
    obj1 = readPatientInfo(patientfile)
    print(obj1.getPatientData())
