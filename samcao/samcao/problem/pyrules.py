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
        self.create_Rules="rules/chinese_rules.cf"

    #返回读取文件的列表
    def readTq(self):
        f=open(self.filename,'r')
        flines=f.readlines()
        for line in flines:
            self.rulease_list.append(line.split('\t'))
        # print self.rulease_list
        return self.rulease_list

    #整理参数的方法
    def zhFunction(self,*argv):
        # print argv
        actionType=argv[0].encode('utf-8').lower()
        rulesType=argv[1].encode('utf-8').lower()
        keyWord=argv[2].encode('utf-8').lower()
        rulesNumber=argv[3].encode('utf-8').lower()
        # print '整理参数'
        return actionType,rulesType,keyWord,rulesNumber

    #根据读取的文件.生成相应的字典
    def rulesDict(self):
        for rulease_one in self.rulease_list:
            # print rulease_one
            if rulease_one[0].lower()=='subject':
                self.subjectDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one
            elif rulease_one[0].lower()=='body':
                self.bodyDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one
    #查询rules
    def searchRules(self,*argv):
        try:
            self.readTq()
            self.rulesDict()
            canSu=self.zhFunction(argv[0],argv[1],argv[2],argv[3])
            self.rulesKey=canSu[1]+'_'+canSu[2]
            if canSu[1]=='body':
                print 'search_body'
                return self.bodyDict[self.rulesKey]
            elif canSu[1]=='subject':
                print 'search_subject'
                print self.subjectDict[self.rulesKey]
                return self.subjectDict[self.rulesKey]
        except KeyError:
            print 'keyError'
            return False
        except Exception,e:
            print e
            return False

    #格式化字典.
    def readDict(self):
        for k,v in self.subjectDict.items():
            self.subjectlist.append(v[0]+'\t'+v[1]+'\t'+v[2])
        for k,v in self.bodyDict.items():
            self.bodylist.append(v[0]+'\t'+v[1]+'\t'+v[2])
        self.bodyrules=''
        for subjectone in self.subjectlist:
            self.bodyrules+=subjectone
        for bodyone in self.bodylist:
            self.bodyrules+=bodyone
        return self.bodyrules

    #写入文件
    def writeFile(self,argv):
        try:
            create_Rules=open(self.filename,'w')
            create_Rules.write(argv)
            create_Rules.close()
        except Exception,e:
            print e

    #删除rules
    def delRules(self,*argv):
        try:
            print 'ok'
            self.readTq()
            self.rulesDict()
            canSu=self.zhFunction(argv[0],argv[1],argv[2],argv[3])
            self.rulesKey=canSu[1]+'_'+canSu[2]
            if canSu[1]=='body':
                print 'del_body'
                del self.bodyDict[self.rulesKey]
            elif canSu[1]=='subject':
                print 'del_subject'
                del self.subjectDict[self.rulesKey]
            self.writeFile(self.readDict())
            return True
        except KeyError:
            print 'keyerror'
            return False
        except Exception,e:
            print e
            return False

    #更改rules
    def updateRules(self,*argv):
        try:
            self.readTq()
            self.rulesDict()
            canSu=self.zhFunction(argv[0],argv[1],argv[2],argv[3])
            self.rulesKey=canSu[1]+'_'+canSu[2]
            if canSu[1]=='body':
                # print 'update_body'
                if self.rulesKey in self.bodyDict.keys():
                    print 'OK_update_body'
                    self.bodyDict[self.rulesKey]=[canSu[1],canSu[2],canSu[3]+'\r\n']
                else:
                    print 'not key_body'
                    return False
            elif canSu[1]=='subject':
                print 'update_subject'
                if self.rulesKey in self.subjectDict.keys():
                    # print 'ok_update_subject'
                    self.subjectDict[self.rulesKey]=[canSu[1],canSu[2],canSu[3]+'\r\n']
                else:
                    print 'not key_subject'
                    return False
            self.writeFile(self.readDict())
            return True
        except KeyError:
            print 'keyError'
            return False
        except Exception,e:
            print e
            return False

    #添加rules
    def addRules(self,*argv):
        try:
            self.readTq()
            self.rulesDict()
            canSu=self.zhFunction(argv[0],argv[1],argv[2],argv[3])
            self.rulesKey=canSu[1]+'_'+canSu[2]
            if canSu[1]=='body':
                # print 'update_body'
                if self.rulesKey in self.bodyDict.keys():
                    print 'OK_add_1'
                    return False
                else:
                    print 'OK_add_2'
                    self.bodyDict[self.rulesKey]=[canSu[1],canSu[2],canSu[3]+'\r\n']
            elif canSu[1]=='subject':
                print 'update_subject'
                if self.rulesKey in self.subjectDict.keys():
                    # print 'ok_update_subject'
                    print 'OK_add_3'
                    return False
                else:
                    print 'OK_add_4'
                    self.subjectDict[self.rulesKey]=[canSu[1],canSu[2],canSu[3]+'\r\n']
            self.writeFile(self.readDict())
            return True
        except KeyError:
            print 'keyError'
            return False
        except Exception,e:
            print e
            return False


    #仅负责写入
    def writeFileDown(self,argv):
        try:
            create_Rules=open(self.create_Rules,'a+')
            create_Rules.write(argv)
            create_Rules.close()
        except Exception,e:
            print e

        #整理文件列表,返回两个字典
    def rulesDict2_down(self):
        for rulease_one in self.rulease_list:
            # print rulease_one
            if rulease_one[0].lower()=='subject':
                self.subjectDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one
            elif rulease_one[0].lower()=='body':
                self.bodyDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one


#根据readTq读取的subjectlist将其写入到chinese_rules.cf文件中.
    def writeSubject(self):
        i=1
        for subject_one in self.subjectDict.values():
            wsub='header CN_SUBJECT_'+str(i)+'\t'+'Subject =~ /'+subject_one[1]+'/\r\n'+'describe CN_SUBJECT_'+str(i)+'\tSubject contains "'+subject_one[1]+'"\r\n'+'score CN_SUBJECT_'+str(i)+'\t'+subject_one[2]+'\r\n'
            self.writeFileDown(wsub)
            i+=1

#根据readTq读取的bodylist将其写入到chinese_rules.cf文件中.
    def writeBody(self):
        i=1
        for body_one in self.bodyDict.values():
            wtbody='body CN_BODY_'+str(i)+'\t'+'/'+body_one[1]+'/\r\n'+'describe CN_BODY_'+str(i)+'\tBody contains "'+body_one[1]+'"\r\n'+'score CN_BODY_'+str(i)+'\t'+body_one[2]+'\r\n'
            self.writeFileDown(wtbody)
            i+=1

#下载功能菜单
    def menuCreateDown(self):

        print 'OK_Menu'
        if os.path.exists(self.create_Rules):
            print 'del_file1'
            os.remove(self.create_Rules)
        print 'del_file2'
        self.readTq()
        print 'readtq'
        self.rulesDict2_down()
        print 'rulesDict2_down'
        self.writeSubject()
        print 'writeSubject'
        self.writeBody()
        print 'writeBody'
        return True