#! /usr/bin/env python
# coding=utf-8
import os,re

def readsinglefile(fobj):

    PatientData = {}
    for line in fobj.readlines():

        if not re.search('\=',line):
            continue
        elif re.search('^DirSize*', line):
            return PatientData
        elif re.search('^  CreateTimeStamp*',line ):
            (key,value) = readSingleValue(line)
            PatientData[key] = value
        elif re.search('CreateTimeStamp',line):
            continue
        else:
            (key, value) = readSingleValue(line)
            PatientData[key] = value

        #return one line
def readSingleValue(str):
    str = str.strip()
    if re.search('\;',str):
        str = str[0:-1]
    str = str.replace("\"",'')
    data = str.split('=')
    return (data[0].strip(), data[1].strip())

# def readSingleField(fobj, index):
#     fieldname = ''
#     fieldvalue = []
#
#     line = fobj.readline()
#     line = line.strip()
#     if ~(line is None):
#         while 1:
#             if line is None or line[0] == '\"' or line[0] == '\/':
#                 line = fobj.readline()
#             else:
#                 break
#
#     if (line is None):
#         pass
#     elif re.search('\=\{$', line):
#         index = index + 1
#         fieldname  = readFieldName(line)
#         while 1:
#             (key,value) = readSingleField(fobj,index)
#             tempdict1 = {}
#             tempdict1[key] = value
#             fieldvalue.append(tempdict1)
#     elif re.search('};$', line):
#         index = index - 1
#         return (fieldname,fieldvalue)
#
#     elif re.search(';$', line):
#         (key, value) = readSingleValue(line)
#         if ~(key is None) and index == 0:
#             return (key, value)
#         else:
#             tempdict2 = {}
#             tempdict2[key] = value
#             fieldvalue.append(tempdict2)
#
#
# #return composite field name
# def readFieldName(str):
#     data = str.split('=')
#     return data[0].strip()
#
# def addSingleField2Struct(Patientdata,name,value):
#     Patientdata[name] = value
#     return Patientdata

if __name__ == "__main__":
    patientfile =  "/Users/yang/Downloads/ESO/Patient_9122/Patient"
    data = readsinglefile(open(patientfile))
    print(data)

