#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: testemail.py

import sys
import os
import imaplib
import time
import re
import cPickle as p

command=("status","qianyi","help")
error_log='errorUser.log'
corr_user='correctuser.txt'
default_dir=os.getcwd()

# def testServer():
# 	try:
# 		M=imaplib.IMAP4(argv[0])
# 		M.logout()
# 		return True
# 	except Exception,ex:
# 		return ex

def runTestOldMailbox(*argv):
    try:
        if argv[3].upper()=='ON':
            testMailServer=imaplib.IMAP4_SSL(argv[0])
        else:
            testMailServer=imaplib.IMAP4(argv[0])
        mLogin=testMailServer.login(argv[1],argv[2])
        # print mLogin
        if mLogin[0]=='OK':
            testMailServer.logout()
            return True
    except Exception,ex:
        return ex

def qiyiold(*argv):
    try:
        print 'start'
        uid_temp_list=[]
        mailbox_temp=""
        oldMailServer=argv[0]
        oldEmailAddress=argv[1]
        oldPassWord=argv[2]
        oldSsl_check=argv[3]

        newMailServer=argv[4]
        newEmailAddress=argv[5]
        newPassWord=argv[6]
        newSsl_check=argv[7]

        if oldSsl_check.upper()=='ON':
            oldemail_M=imaplib.IMAP4_SSL(oldMailServer)
        else:
            oldemail_M=imaplib.IMAP4(oldMailServer)

        if newSsl_check.upper()=='ON':
            newemail_M=imaplib.IMAP4_SSL(newMailServer)
        else:
            newemail_M=imaplib.IMAP4(newMailServer)

        oldemail_M.login(oldEmailAddress,oldPassWord)
        newemail_M.login(newEmailAddress,newPassWord)

        maildir_l=mail_dir(oldemail_M.list())
        userNumMail=0
        userAllMail=0
        oldemail_M.noop()
        newemail_M.noop()

        for mailbox in maildir_l:
            userNumMail=int(oldemail_M.select(mailbox)[1][0])
            userAllMail+=userNumMail
            print '<%s> <%s> <%s>'%(oldEmailAddress,mailbox,userNumMail)
        print 'User: <%s> EmailNum: <%s>.'%(oldEmailAddress,userAllMail)

        print 'Start qianyi mail....'

        for mailbox in maildir_l:
            oldemail_M.select(mailbox)
            #判断是否存在文件夹,不存在则进行创建
            if newemail_M.select(mailbox)[0]<>'OK':
                print 'Not mailbox <%s>, Create mailbox <%s>.'%(mailbox,newemail_M.create(mailbox)[1])
                # newemail_M.create(mailbox)
                newemail_M.select(mailbox)


            old_typ_n,old_data_n=newemail_M.search(None,'ALL')
            oldmailid_n=old_data_n[0].split()
            userNumMail=int(oldemail_M.select(mailbox)[1][0])
            uidlist = panDuanUserBox(oldMailServer,oldEmailAddress,mailbox)
            uid_temp_list=uidlist
            typ,data=oldemail_M.search(None,'SEEN')
            for num in data[0].split():
                typ,datauid=oldemail_M.fetch(num,'UID')
                uid=datauid[0].split(' ')[2][0:-1]
                if (uid in uidlist):
                    continue
                else:
                    print 'Start downloading...<%s><%s>'%(mailbox,num)
                    #实现无痕取信,不影响原来服务器上面邮箱中邮件的状态
                    typ,mdata=oldemail_M.fetch(num,'(UID BODY.PEEK[])')
                    print 'download success...'
                    print 'Start upload...'

                    if len(mdata[0][1])<1:
                        print '<%s> mailbox,num <%s> len=0,continue.'%(mailbox,num)
                        continue
                    newemail_M.select(mailbox)
                    try:
                        newemail_M.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
                    except Exception,ex:
                        print 'upload error:<%s><%s><%s><%s>'%(oldEmailAddress,mailbox,num,ex)
                    uidlist.append(uid)
                    uid_temp_list=uidlist

            new_typ_n,new_data_n=newemail_M.search(None,'ALL')
            newmailid_n=new_data_n[0].split()
            datalist=list(set(oldmailid_n)^set(newmailid_n))
            for num in datalist:
                newemail_M.store(num,'+FLAGS','\SEEN')
            typ,data=oldemail_M.search(None,'UNSEEN')

            for num in data[0].split():
                typ,datauid=oldemail_M.fetch(num,'UID')
                uid=datauid[0].split(' ')[2][0:-1]
                if(uid in uidlist):
                    continue
                else:
                    print 'Start downloading...<%s><%s>'%(mailbox,num)
                    typ,mdata=oldemail_M.fetch(num,'(UID BODY.PEEK[])')
                    print 'download success...'
                    print 'Start upload...'
                    if len(data[0][1])<1:
                        print '<%s> mailbox,num <%s> len=0,continue.'%(mailbox,num)
                        continue
                    newemail_M.select(mailbox)
                try:
                    newemail_M.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
                except Exception,ex:
                    print 'upload error:<%s><%s><%s><%s>'%(oldEmailAddress,mailbox,num,ex)
                uidlist.append(uid)
                uid_temp_list=uidlist
            writeuid(oldMailServer,oldEmailAddress,mailbox,uidlist)
        return True
    except Exception,ex:
        return ex
    finally:
        writeuid(oldMailServer,oldEmailAddress,mailbox,uid_temp_list)



#将UID写入到文件中.以做记录
def writeuid(oldserver,oldname,mailbox,uidlist):
    # print os.getcwd()
    temppath=os.path.join(default_dir,'temp').replace('\\','/')
    os.chdir(temppath)
    filename=oldname+mailbox
    f=file(filename,'w')
    p.dump(uidlist,f)
    f.close()
    os.chdir(default_dir)


##判断是否有此文件夹
def panDuanUserBox(*argv):
	uidlist=[]
	# print '-------------------------------'
	# print default_dir
	# os.chdir(default_dir)
	temppath=os.path.join(default_dir,'temp').replace('\\','/')
	# print os.getcwd()
	if(os.path.exists(temppath)):
		os.chdir(temppath)
		filename=argv[1]+argv[2]
		if(os.path.isfile(filename)):
			f=file(filename)
			uidlist=p.load(f)
			os.chdir(default_dir)
			return uidlist
		else:
			os.chdir(default_dir)
			return uidlist
	else:
		os.mkdir('temp')
		os.chdir(default_dir)
		return uidlist

#用于排列邮件夹列表
def mail_dir(mlist):
    mail_list=[]
    for listone in mlist[1]:
        mail_list.append(listone.strip('"').split('"')[-1].strip(' '))
    return mail_list

