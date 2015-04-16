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
        try:
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
        except Exception,e:
            print e

    def readBody(self):
        try:
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
        except Exception,e:
            print e

    def writeRules(self,*argv):
        try:
            fwrite_chinese=open(self.wtchinese_rules,'a+')
            for line in argv:
                fwrite_chinese.write(line[0]+"\t"+line[1]+"\t"+line[2]+"\n")
            fwrite_chinese.close()
        except Exception,e:
            print e

    def menuReadRules(self):
        self.subjectList=self.readSubject()
        for subject_one in self.subjectList:
            self.writeRules(subject_one)
        self.bodyList=self.readBody()
        for body_one in self.bodyList:
            self.writeRules(body_one)
        print 'success'

#根据jl_wtchinese_rules 生成chinese_rules.cf文件.
class createRules:
    def __init__(self):
        self.filename="rules/jl_wtchinese_rules.txt"
        self.subjectList=[]
        self.bodyList=[]
        self.create_Rules="rules/chinese_rules.cf"

#读取jl_wtchinese_rules.txt文件.根据每行的第一个单词,判断是body还是subject.生成bodylist与subjectlist
    def readTq(self):
        f=open(self.filename,'r')
        flines=f.readlines()
        for line in flines:
            if line.split('\t')[0]=='subject':
                self.subjectList.append(line)
            elif line.split('\t')[0]=='body':
                self.bodyList.append(line)
        # print self.subjectList
        # print self.bodyList

#根据readTq读取的subjectlist将其写入到chinese_rules.cf文件中.
    def writeSubject(self):
        i=1
        for subject_one in self.subjectList:
            subjectName=subject_one.split('\t')[1]
            subjectNumber=subject_one.split('\t')[2]
            wsub='header CN_SUBJECT_'+str(i)+'\t'+'Subject =~ /'+subjectName+'/\r\n'+'describe CN_SUBJECT_'+str(i)+'\tSubject contains "'+subjectName+'"\r\n'+'score CN_SUBJECT_'+str(i)+'\t'+subjectNumber+"\r\n"
            self.writeFile(wsub)
            i+=1

#根据readTq读取的bodylist将其写入到chinese_rules.cf文件中.
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

#将相关的信息写入到chinese_rules.cf文件中.
#仅负责写入
    def writeFile(self,argv):
        try:
            create_Rules=open(self.create_Rules,'a+')
            create_Rules.write(argv)
            create_Rules.close()
        except Exception,e:
            print e

#读写功能的顺序菜单.
    def menuCreateRules(self):
        self.readTq()
        self.writeSubject()
        self.writeBody()

    def readUserPrint(self):
        userPrint_Type = raw_input("请输入需要添加的类型<Body/Subject>: ")
        userPrint_Word=raw_input("请输入需要添加的关键词: ")
        userPrint_Number=raw_input("请输入分值: ")
        print userPrint_Type,userPrint_Word,userPrint_Number
        body_jl=[]
        subject_jl=[]
        if userPrint_Type.upper()=='BODY':
            for bodyOne in self.bodyList:
                # while userPrint_Word in bodyOne.split('\t')[1]:
                    # print bodyOne
                if userPrint_Word in bodyOne.split('\t')[1]:
                    body_jl.append(bodyOne)
            if len(body_jl)<1:
                print 'OK'
            else:
                print body_jl
        elif userPrint_Type.upper()=="SUBJECT":
            for subjectOne in self.subjectList:
                if userPrint_Word in subjectOne.split('\t')[1]:
                    subject_jl.append(subjectOne)
            if len(subject_jl)<1:
                print 'OK'
            else:
                print subject_jl

    def returnRulesList(self):
        try:
            ruleslist=[]
            f=open(self.filename,'r')
            flines=f.readlines()
            for line in flines:
                ru_e=line.split('\t')
                if ru_e[0]=='subject' or ru_e[0]=='body':
                    ruleslist.append(ru_e)
            return ruleslist
        except Exception,e:
            return e



if __name__=="__main__":
    cr=createRules()
    # cr.readUserPrint()
    # print cr.returnRulesList()
    # cr.readUserPrint()

