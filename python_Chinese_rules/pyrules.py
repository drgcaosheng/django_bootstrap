#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: pyrules.py

import os,sys,codecs,re
f=open('Chinese_rules.cf','r')
regex_subject=re.compile(r'header CN_SUBJECT_.{1,8}Subject =~ /(.{1,50})/')
regex_number=re.compile(r'score CN_SUBJECT_.{1,8}	(.{1,5})')
flines=f.readlines()

for line in flines:
    # if re.search(r'header CN_SUBJECT_',line):
    #     print "subject\t"+regex_subject.findall(line)[0]
    # if re.search(r'score CN_SUBJECT_',line):
    #     print regex_number.findall(line)[0]
    print regex_subject.findall(line)

f.close()


