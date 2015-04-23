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