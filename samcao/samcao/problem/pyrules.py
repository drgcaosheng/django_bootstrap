#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: pyrules.py

import os,sys,codecs,re


class createRules:
    def __init__(self):
        self.filename="rules/jl_wtchinese_rules.txt"
        self.rulease_list=[]
        self.subjectDict={}
        self.bodyDict={}
        self.subjectlist=[]
        self.bodylist=[]

    def readTq(self):
        f=open(self.filename,'r')
        flines=f.readlines()
        for line in flines:
            self.rulease_list.append(line.split('\t'))
        # print self.rulease_list
        return self.rulease_list

    def zhFunction(self,*argv):
        # print argv
        actionType=argv[0].encode('utf-8').lower()
        rulesType=argv[1].encode('utf-8').lower()
        keyWord=argv[2].encode('utf-8').lower()
        rulesNumber=argv[3].encode('utf-8').lower()
        # print '整理参数'
        return actionType,rulesType,keyWord,rulesNumber

    def rulesDict(self):
        for rulease_one in self.rulease_list:
            # print rulease_one
            if rulease_one[0].lower()=='subject':
                self.subjectDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one
            elif rulease_one[0].lower()=='body':
                self.bodyDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one

    def searchRules(self,*argv):
        try:
            self.readTq()
            self.rulesDict()
            canSu=self.zhFunction(argv[0],argv[1],argv[2],argv[3])
            self.rulesKey=canSu[1]+'_'+canSu[2]
            if canSu[1]=='body':
                # print 'search_body'
                return self.bodyDict[self.rulesKey]
            elif canSu[1]=='subject':
                # print 'search_subject'
                # print self.subjectDict[self.rulesKey]
                return self.subjectDict[self.rulesKey]
        except KeyError:
            # print 'keyError'
            return False
        except Exception,e:
            # print e
            return False


