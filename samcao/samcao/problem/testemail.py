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

def testServer():
	try:
		M=imaplib.IMAP4(argv[0])
		M.logout()
		return True
	except Exception,ex:
		return ex

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


#迁移邮箱的方法
# def qiyiold(*argv):
#     uid_temp_list=[]
#     mailbox_temp=""
#     try:
#         if argv[3].upper()=='ON':
#             testMailServer=imaplib.IMAP4_SSL(argv[0])
#         else:
#             testMailServer=imaplib.IMAP4(argv[0])
#         M=imaplib.IMAP4(argv[0])
#         M.login(argv[1],argv[2])
#         N=imaplib.IMAP4(argv[3])
#         N.login(argv[4],argv[5])
#         maildir_l=mail_dir(M.list())
#         userNumMail=0
#         userAllMail=0
#         M.noop()
#         N.noop()
#         for mailbox in maildir_l:
#             userNumMail=int(M.select(mailbox)[1][0])
#             userAllMail+=userNumMail
#             print '<%s> <%s> <%s>'%(argv[1],mailbox,userNumMail)
#             print 'User: <%s> EmailNum: <%s>.'%(argv[1],userAllMail)
#
#         print 'Start qianyi mail....'
#
#         for mailbox in maildir_l:
#             # print mailbox
# 			M.select(mailbox)
#             if N.select(mailbox)[0]<>'OK':
#                 print 'Not mailbox <%s>, Create mailbox <%s>.'%(mailbox,N.create(mailbox)[1])
#                 N.select(mailbox)
#             # N.select(mailbox)
# 			#
# 			# 此步更新于20140813
# 			old_typ_n,old_data_n=N.search(None,'ALL')
#             oldmailid_n=old_data_n[0].split()
#             userNumMail=int(M.select(mailbox)[1][0])
#             uidlist = panDuanUserBox(argv[0],argv[1],mailbox)
#             uid_temp_list=uidlist
#             typ,data=M.search(None,'SEEN')
#             #print 'seen-------'
#             for num in data[0].split():
#                 # print num
#                 typ,datauid=M.fetch(num,'UID')
#                 uid=datauid[0].split(' ')[2][0:-1]
#                 if(uid in uidlist):
#                     continue
#                 else:
#                     print 'Start downloading...<%s><%s>'%(mailbox,num)
#                     #实现无痕取信,不影响原来服务器上面邮箱中邮件的状态
#                     typ,mdata=M.fetch(num,'(UID BODY.PEEK[])')
#                     print 'download success...'
#                     print 'Start upload...'
#                     # print '01'
#                     if len(mdata[0][1])<1:
#                         print '<%s> mailbox,num <%s> len=0,continue.'%(mailbox,num)
#                         continue
#                     try:
#                         # print mailbox
# 						# print '03'
# 						N.select(mailbox)
#                     except Exception,ex:
#                         print '<%s><%s><%s>email error!!!'%(argv[0],mailbox,num)
#                         N=imaplib.IMAP4(argv[3])
#                         N.login(argv[4],argv[5])
#                         N.select(mailbox)
#                     # print '02'
#                     try:
#                         N.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
#                     except Exception,ex:
#                         print 'upload error:<%s><%s><%s><%s>'%(argv[1],mailbox,num,ex)
#                     uidlist.append(uid)
#                     uid_temp_list=uidlist
#
#             #此步更新于20140813
#             new_typ_n,new_data_n=N.search(None,'ALL')
#             newmailid_n=new_data_n[0].split()
#             datalist=list(set(oldmailid_n)^set(newmailid_n))
#             #
#
#             #typ,data=N.search(None,'ALL')
#             # for num in data[0].split():
#             for num in datalist:
#                 N.store(num,'+FLAGS','\SEEN')
#             typ,data=M.search(None,'UNSEEN')
#             # print 'unseen--------'
#             # for num in data[0].split():
#             	# print num
#             	# typ,mdata=M.fetch(num,'(UID BODY.PEEK[])')
#             	# N.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
#
#             for num in data[0].split():
#                 # print num
#                 typ,datauid=M.fetch(num,'UID')
#                 uid=datauid[0].split(' ')[2][0:-1]
#                 if(uid in uidlist):
#                     continue
#                 else:
#                     print 'Start downloading...<%s><%s>'%(mailbox,num)
#                     typ,mdata=M.fetch(num,'(UID BODY.PEEK[])')
#                     print 'download success...'
#                     print 'Start upload...'
#                     if len(data[0][1])<1:
#                         print '<%s> mailbox,num <%s> len=0,continue.'%(mailbox,num)
#                         continue
#                     try:
#                         N.select(mailbox)
#                     except Exception,ex:
#                         print '<%s><%s><%s>email error!!!'%(argv[0],mailbox,num)
#                         N=imaplib.IMAP4(argv[3])
#                         N.login(argv[4],argv[5])
#                         N.select(mailbox)
#                     try:
#                         N.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
#                     except Exception,ex:
#                         print 'upload error:<%s><%s><%s><%s>'%(argv[1],mailbox,num,ex)
#                     uidlist.append(uid)
#                     uid_temp_list=uidlist
#
#             print ('<%s><%s>OK'%(argv[1],mailbox))
#             writeuid(argv[0],argv[1],mailbox,uidlist)
#             # M.close()
#             # N.close()
#             # M.logout()
#             # N.logout()
#             return True
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

