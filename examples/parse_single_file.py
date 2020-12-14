#!/usr/bin/env python
# coding=utf-8
import os
import pinnacle3tps2json as pinn
import re
from dotmap import DotMap
import pickle


def readPlanTrial(patientPlanDir):
    """
    Read all the information out of a plan.Trial file for a given patient plan directory.
    """
    #data = pinn.read(os.path.join(patientPlanDir,'Plan_4/plan.Bolus'))
    escape_list = ['json','img','dcm','Machines','Command','OrbitBioObjectives']
    for paths, dirs, files in os.walk(patientPlanDir):
        for file in files:
            if os.path.splitext(file)[1][1:] in escape_list or re.search('binary',file)or re.search('Orbit',file):
                continue
            if os.path.isfile(os.path.join(paths, file)):
                print(os.path.join(paths, file))
                data = pinn.read(os.path.join(paths, file))

    print('end')
    return data


if __name__ == '__main__':
    patientPlanDir = '/home/peter/PinnWork/Patient_26482/'

    planTrial = readPlanTrial(patientPlanDir)
