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
        self.filename="jl_wtchinese_rules.txt"
        self.subjectList=[]
        self.bodyList=[]
        self.create_Rules="chinese_rules.cf"
        self.rulease_list=[]
        self.bodyDict={}
        self.subjectDict={}

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

    def searchRules(self,*argv):
        # print argv
        canSu=self.zhFunction(argv[0],argv[1],argv[2])
        # print canSu
        # rulesType=rulesType.encode('utf-8').lower()
        # keyWord=keyWord.encode('utf-8').lower()
        # rulesNumber=rulesNumber.encode('utf-8').lower()
        try:
            if canSu[0]=='body':
                return self.bodyDict[canSu[1]]
            elif canSu[0]=='subject':
                return self.subjectDict[canSu[1]]
        except KeyError:
            return False
        except Exception,e:
            return e

    def zhFunction(self,*argv):
        # print argv
        rulesType=argv[0].encode('utf-8').lower()
        keyWord=argv[1].encode('utf-8').lower()
        rulesNumber=argv[2].encode('utf-8').lower()
        # print '整理参数'
        return rulesType,keyWord,rulesNumber

    def addRules(self,*argv):
        canSu=self.zhFunction(argv[0],argv[1],argv[2])
        # print '===='
        # print canSu
        # print '========'

    #读取jl_wtchinese_rules.txt文件.返回一个列表
    def readTq(self):
        f=open(self.filename,'r')
        flines=f.readlines()
        for line in flines:
            self.rulease_list.append(line.split('\t'))
        return self.rulease_list
    def rulesDict(self):
        for rulease_one in self.rulease_list:
            if rulease_one[0].lower()=='subject':
                self.subjectDict[rulease_one[1]]=rulease_one
            elif rulease_one[0].lower()=='body':
                self.bodyDict[rulease_one[1]]=rulease_one


class createRules2:
    def __init__(self):
        self.filename="jl_wtchinese_rules.txt"
        self.rulease_list=[]
        self.subjectDict={}
        self.bodyDict={}
        self.subjectlist=[]
        self.bodylist=[]

    #获取传递过来的参数,或者也叫整理参数
    def inputRules(self):
        typeRules=raw_input("Please input Type <body/subject> :")
        keyWordRules=raw_input("Please input keyWord: ")
        numberRules=raw_input("Please input number: ")
        if typeRules.lower()=="body" or typeRules.lower()=="subject":
            print typeRules,keyWordRules,numberRules
        else:
            return "type_error"

    #读取文件.返回文件列表
    def readTq(self):
        f=open(self.filename,'r')
        flines=f.readlines()
        for line in flines:
            self.rulease_list.append(line.split('\t'))
        return self.rulease_list

    #整理文件列表,返回两个字典
    def rulesDict(self):
        for rulease_one in self.rulease_list:
            # print rulease_one
            if rulease_one[0].lower()=='subject':
                self.subjectDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one
            elif rulease_one[0].lower()=='body':
                self.bodyDict[rulease_one[0]+'_'+rulease_one[1]]=rulease_one
    #查询
    def searchRules(self,typeRules,keyWord,numberRules):
        try:
            self.rulesKey=typeRules+'_'+keyWord
            if typeRules.lower()=='body':
                return self.bodyDict[self.rulesKey]
            elif typeRules.lower()=='subject':
                return self.subjectDict[self.rulesKey]
        except KeyError:
            return False
        except Exception,e:
            return e

    #添加
    def addRules(self,typeRules,keyWord,numberRules):
        self.rulesKey=typeRules+'_'+keyWord
        print 'OK'
        search_key=self.searchRules(typeRules,keyWord,numberRules)
        if isinstance(search_key,list):
            print 'list'
        else:
            if typeRules.lower()=='body':
                self.bodyDict[self.rulesKey]=[typeRules,keyWord,numberRules+'\r\n']
            elif typeRules.lower()=='subject':
                self.subjectDict[self.rulesKey]=[typeRules,keyWord,numberRules+'\r\n']
            print 'add_ok'
        print self.bodyDict,self.subjectDict

    #更改
    def updateRules(self,typeRules,keyWord,numberRules):
        self.rulesKey=typeRules+'_'+keyWord
        search_key=self.searchRules(typeRules,keyWord,numberRules)
        if isinstance(search_key,list):
            if typeRules.lower()=='body':
                self.bodyDict[self.rulesKey]=[typeRules,keyWord,numberRules+'\r\n']
                # print self.bodyDict
                return True
            elif typeRules.lower()=='subject':
                self.subjectDict[self.rulesKey]=[typeRules,keyWord,numberRules+'\r\n']
                # print self.subjectDict
                return True
        else:
            return False

    #删除
    def delRules(self,typeRules,keyWord,numberRules):
        try:
            self.rulesKey=typeRules+'_'+keyWord
            if typeRules.lower()=='body':
                del self.bodyDict[self.rulesKey]
            elif typeRules.lower()=='subject':
                del self.subjectDict[self.rulesKey]
        except KeyError:
            return False
        except Exception,e:
            return e

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


if __name__=="__main__":
    cr=createRules2()
    print cr.readTq()
    # cr.rulesDict()
    # print cr.searchRules('subject','优惠','1.2')
    # print cr.addRules('subject','优惠优惠优惠优惠','1.2222')
    # cr.updateRules('subject','优惠','333')
    # cr.delRules('subject','优惠','333')
    # print cr.subjectDict
    # print cr.readDict()
    # cr.inputRules()
    # print cr.searchRules(u'body',u'有限公司',u'2')
    # print cr.addRules(u'body',u'有限公司',u'2')

