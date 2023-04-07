#!/usr/bin/env python3
from __future__ import print_function
from datetime import datetime
import odrive
from odrive.enums import *
import time
import math
import sys
import json
import os


def run_bash_command(cmd: str):
    import subprocess

    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise Exception(error)
    else:
        return output


def BackupConfig():
    run_bash_command("odrivetool backup-config " + filename)


def cloneConfig(axis_source, axis_target):
    axisConfig = None
    f = open(filename)
    data = json.load(f)
    for i in data:
        if i == axis_source:
            axisConfig = data[i]

    for i in data:
        if i == axis_target:
            data[i] = axisConfig


    jsonContent = json.dumps(data)

    #remove if exist
    if os.path.exists("newConfig.json"):
        os.remove("newConfig.json")

    finalFinal = open('newConfig.json', 'w')
    finalFinal.write(jsonContent)

    f.close()
    finalFinal.close()

def loadNewConfig():
    run_bash_command("odrivetool restore-config newConfig.json")
    #remove if exist
    if os.path.exists("newConfig.json"):
        os.remove("newConfig.json")


'''
Start Here
'''
filename = "/home/edog/Robot/Odrive/backups/BackupClone_" + datetime.now().strftime("%Y%m%d") + ".json"
BackupConfig()


axis_source = sys.argv[1]
if axis_source == 'axis0':
    axis_target = 'axis1'
    print("clone axis0 to axis1")
elif axis_source == 'axis1':
    print("clone axis1 to axis0")
    axis_target = 'axis0'
else:
    exit("Error, unknown config")

cloneConfig(axis_source, axis_target)
loadNewConfig();
