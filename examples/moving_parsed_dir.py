#! /usr/bin/env python
# coding=utf-8
# using a logfile (findedfile) finded parsed file in sourcepath, then copy it to target path

import os,re
#这是一个测试
import filetype
import shutil


if __name__ == "__main__":
    sourcepath = '/Volumes/PinnSETemp/NewPatients/Institution_3856/Mount_0/'
    targetpath = '/Volumes/PinnSETemp/ESO2Mat/'
    findedfile = '/Volumes/PinnSETemp/ESO2Mat/16-Oct-2017_log.log'
    listfile   = "/Volumes/PinnSETemp/ESO2Mat/listfile2.log"
    findedobj  = open(findedfile)
    outobj = open(listfile,'w')
    findedlist = []
    for line in findedobj.readlines():
        objlist = line.split('\t')
        findedlist.append(objlist[2])

    for curdir in os.listdir(sourcepath):
        if curdir == '.' or curdir == '..':
            continue
        elif re.match('Patient_\d+',curdir):
            dirname = curdir.strip().split('_')
            if dirname[-1] in findedlist:
                sourcedir = os.path.join(sourcepath,curdir)
                print sourcedir
                shutil.move(sourcedir,targetpath)
                outobj.write(curdir)
    outobj.close()
    print "end"
