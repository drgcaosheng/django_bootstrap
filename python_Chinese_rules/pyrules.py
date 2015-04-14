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
        self.search_header="header CN_SUBJECT_"
        self.search_body="body CN_BODY_"
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
                self.alistone.append(self.regex_subject.findall(line)[0])
            if not re.search(self.regex_subnumber,line):
                continue
            self.alistone.append(self.regex_subnumber.findall(line)[0])
            self.alist.append(self.alistone)
            self.alistone=[]
        f.close()
        return self.alist

    def readBody(self):
        f=open(self.chinese_rules_file,'r')
        flines=f.readlines()
        for line in flines:
            if re.search(self.search_body,line):
                # print 'body'
                self.alistone.append("body")
                # print self.regex_body.findall(line)[0]
                self.alistone.append(self.regex_body.findall(line)[0])
            if not re.search(self.regex_body_number,line):
                continue
            # print self.regex_body_number.findall(line)[0]
            self.alistone.append(self.regex_body_number.findall(line)[0])
            self.alist.append(self.alistone)
            self.alistone=[]
        f.close()
        return self.alist

    def writeRules(self,*argv):
        fwrite_chinese=open(self.wtchinese_rules,'a+')
        for line in argv:
            fwrite_chinese.write(line[0]+"\t"+line[1]+"\t"+line[2]+"\n")
        fwrite_chinese.close()

    def menuReadRules(self):
        self.subjectList=self.readSubject()
        for subject_one in self.subjectList:
            self.writeRules(subject_one)
        self.bodyList=self.readBody()
        for body_one in self.bodyList:
            self.writeRules(body_one)

class createRules:
    def __init__(self):
        self.filename="jl_wtchinese_rules.txt"
        self.subjectList=[]
        self.bodyList=[]
        self.create_Rules="chinese_rules.cf"

    def readTq(self):
        f=open(self.filename,'r')
        flines=f.readlines()
        for line in flines:
            if line.split('\t')[0]=='subject':
                self.subjectList.append(line)
            elif line.split('\t')[0]=='body':
                self.bodyList.append(line)

    def writeSubject(self):
        i=1
        for subject_one in self.subjectList:
            subjectName=subject_one.split('\t')[1]
            subjectNumber=subject_one.split('\t')[2]
            wsub='header CN_SUBJECT_'+str(i)+'\t'+'Subject =~ /'+subjectName+'/\r\n'+'describe CN_SUBJECT_'+str(i)+'\tSubject contains "'+subjectName+'"\r\n'+'score CN_SUBJECT_'+str(i)+'\t'+subjectNumber+"\r\n"
            self.writeFile(wsub)
            i+=1

    def writeBody(self):
        i=1
        # print self.bodyList
        for body_one in self.bodyList:
            # print body_one
            bodyName=body_one.split('\t')[1]
            bodyNumber=body_one.split('\t')[2]
            wtbody='body CN_BODY_'+str(i)+'\t'+'/'+bodyName+'/\r\n'+'describe CN_BODY_'+str(i)+'\tBody contains "'+bodyName+'"\r\n'+'score CN_BODY_'+str(i)+'\t'+bodyNumber+"\r\n"
            self.writeFile(wtbody)
            # print 'body CN_BODY_'+str(i)+'\t'+'/'+bodyName+'/'
            # print 'describe CN_BODY_'+str(i)+'\tBody contains "'+bodyName+'"'
            # print 'score CN_BODY_'+str(i)+'\t'+bodyNumber
            i+=1
    def writeFile(self,argv):
        print argv
        create_Rules=open(self.create_Rules,'a+')
        # for line in argv:
        create_Rules.write(argv)
        #     create_Rules.write(argv[0])
        create_Rules.close()




if __name__=="__main__":
    cr=createRules()
    cr.readTq()
    cr.writeSubject()
    cr.writeBody()
    # cr.test()
    # tq=tiquchinese()
    # tq.menuReadRules()

