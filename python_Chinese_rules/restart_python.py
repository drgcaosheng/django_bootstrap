#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: restart_python.py

import subprocess,os

# tasklist = subprocess.call('TASKLIST /M python*')
# print tasklist
try:
    tasklist = subprocess.Popen('taskkill /F /IM python.exe',shell=True)
except:
    print 'a'

# print tasklist.returncode
# for task in tasklist:
#     print task