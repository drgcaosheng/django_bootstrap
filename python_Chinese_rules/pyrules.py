#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: pyrules.py

import os,sys,codecs,re
f=open('Chinese_rules.cf','r')
# re.search(r'header CN_SUBJECT',line):
regex=re.compile(r'header CN_SUBJECT_\d{1,5}	Subject =~ /(.{1,50})/')
alist=[]
flines=f.readlines()
a=1
for line in flines:
    if re.search(r'header CN_SUBJECT_',line):
        print line+str(a),
        a+=1

# for line in flines:
#     alist.append(regex.findall(line),)
# a=1
# for i in alist:
#     if len(i)>0:
#         print a
#         print i[0]
#         a+=1


f.close()