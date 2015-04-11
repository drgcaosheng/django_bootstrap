#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: pyrules.py

import os,sys,codecs,re
class tiquchinese:
    def __init__(self):
        self.regex_subject=re.compile(r'header CN_SUBJECT_.{1,8}Subject =~ /(.{1,50})/')
        self.regex_body=re.compile(r'body CN_BODY_.{1,8}/(.{1,60})/')
        self.regex_subnumber=re.compile(r'score CN_SUBJECT_.{1,8}	(.{1,5})')
        self.regex_body_number=re.compile(r'score CN_BODY_.{1,8}	(.{1,5})')
                # regex_number=re.compile(r'score CN_SUBJECT_.{1,8}	(.{1,5})')
        self.search_header="header CN_SUBJECT_"
        self.search_body="score CN_SUBJECT_"
        self.alist=[]
        self.alistone=[]
        self.chinese_rules_file="chinese_rules.cf"
        self.wtchinese_rules="jl_wtchinese_rules.txt"

    def readSubject(self):
        f=open(self.chinese_rules_file,'r')
        flines=f.readlines()
        for line in flines:
            if re.search(self.search_header,line):
                self.alistone.append("subject")
                # print "subject"
                self.alistone.append(self.regex_subject.findall(line)[0])
                # print self.regex_subject.findall(line)[0]
            if not re.search(self.regex_subnumber,line):
                continue
            # print self.regex_subnumber.findall(line)[0]
            # print line

            self.alistone.append(self.regex_subnumber.findall(line)[0])
            self.alist.append(self.alistone)
            self.alistone=[]
        print self.alist
        f.close()
'''
        for line in flines:
            if re.search(self.search_body,line):
                self.alistone.append("body")
                self.alistone.append(self.regex_body_number.findall(line)[0])
            if not re.search(self.regex_body_number,line):
                continue
            self.alistone.append(self.regex_body_number.findall(line)[0])
            self.alist.append(self.alistone)
            self.alistone=[]
'''


if __name__=="__main__":
    tq=tiquchinese()
    tq.readSubject()



# f=open('Chinese_rules.cf','r')
# regex_subject=re.compile(r'header CN_SUBJECT_.{1,8}Subject =~ /(.{1,50})/')
# regex_body=re.compile(r'body CN_BODY_.{1,8}/(.{1,60})/')
# regex_number=re.compile(r'score CN_SUBJECT_.{1,8}	(.{1,5})')
# regex_body_number=re.compile(r'score CN_BODY_.{1,8}	(.{1,5})')
# flines=f.readlines()
# alist=[]
# alistone=[]
'''
for line in flines:
    if re.search(r'header CN_SUBJECT_',line):
        alistone.append("subject")
        alistone.append(regex_subject.findall(line)[0])
        # print "subject\t"+regex_subject.findall(line)[0]
        # continue
    if not re.search(r'score CN_SUBJECT_',line):
        continue
    alistone.append(regex_number.findall(line)[0])
        # print regex_number.findall(line)[0]
    alist.append(alistone)
    alistone=[]


for line in flines:
    if re.search(r'body CN_BODY_',line):
        alistone.append("body")
        alistone.append(regex_body.findall(line)[0])
    if not re.search(r'score CN_BODY_',line):
        continue
    alistone.append(regex_body_number.findall(line)[0])
    alist.append(alistone)
    alistone=[]
f.close()


fwrite_chinese=open('bt.txt','wb')
for i in alist:
    fwrite_chinese.write(i[0]+"\t"+i[1]+"\t"+i[2]+"\n")
fwrite_chinese.close()

'''





