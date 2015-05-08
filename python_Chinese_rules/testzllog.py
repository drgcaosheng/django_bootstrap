#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filenaem: testzllog.py
import re,os

f=open(r'0508.txt','r')
a=f.readlines()
b=[]
print '原文件:'
print a
# for aline in a:
#     b.append(re.sub(r'Fri',r'\r\nFri',aline))
for aline in a:
    b.append(re.sub(r'Fri','\nFri',aline))
f.close()
print '替换换行后的文件:'
print b
for i in b:
    print i,