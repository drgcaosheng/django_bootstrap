#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: qyemail.py
#Version=0.1
#Date=2014.07.26
#Name: samcao
#Email: drgcaosheng@163.com

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

def Menu():
	try:
		# print sys.argv
		# print len(sys.argv)
		if(len(sys.argv)==1):
			print '\n>>Please run index.py help'
			Help()
			sys.exit()
		#判断命令是否正确的
		if(sys.argv[1] in command):
			#如果是帮助的话.则输出帮助信息,并退出
			if(sys.argv[1]==command[2]):
				Help()
				sys.exit()
			#上面已经判断是在command中.则判断文件是否正常.并且不为空
			if(len(sys.argv)<3):
				print '\n>>Please input filename.'
				Help()
				sys.exit()
			if(os.path.isfile(sys.argv[2])):
				if(sys.argv[1]==command[0]):
					#command[0](sys.argv[2])
					Status(sys.argv[2],command[0])
					# print 'error'
				else:
					Qianyi(sys.argv[2],command[1])
			else:
				print 'Not filename [ %s ] !!! Make sure the file name is correct.' %sys.argv[2]
		else:
			print '\nCommand Error!!! \nPlease run >python py.exe help'
			Help()
			sys.exit()
	except KeyboardInterrupt:
		print 'CTRL+C\nQuit!'
	# except IndexError:
	# 	print 'Please run index.py help'
	except EOFError:
		print 'Force Quit!!!'


#确定是否迁移
def Qianyi(*argv):
	#检查用户名密码相关是否正确
	statuslist=Status(argv[0],argv[1])
	running=True
	# print argv[0].argv[1]
	# sys.exit()
	#判断是否有错误的帐号信息
	if statuslist[1]>0:
		while running:
			#判断是否继续迁移
			qyIf=raw_input('Have %s error user,migrate <y/n> :'%statuslist[1])
			if qyIf=='y' or qyIf=='Y':
				startQianyi(corr_user)
				running=False
			elif qyIf=='n' or qyIf=='N':
				print 'Please Check Username or Password!!!'
				sys.exit()
	else:
		startQianyi(corr_user)


#迁移的菜单.显示迁移至那个用户
def startQianyi(*argv):
	# print argv
	userlist=readName(argv[0])
	print 'Total number of subscribers %s: ' %len(userlist)
	# print "Calculate the number of all messages..."
	# print argv[0]
	# sys.exit()
	# allemailnum=allmail(argv[0])
	# sys.exit()
	# print 'All Mail Num: %s' %allemailnum
	mailnum=0
	for user in userlist:
		mailnum+=1
		oldServer=user[0]
		oldName=user[1]
		oldPass=user[2]
		newServer=user[3]
		newName=user[4]
		newPass=user[5]
		ifQianYi=re.sub(r'\n','',user[6])
		ifQianYi=re.sub(r'\r','',ifQianYi)
		#判断是否需要迁移
		if ifQianYi.upper()=='NO':
			print 'Mail account %s does not need to migrate'% oldName
			mailnum+=1
			continue
		#开始进入迁移
		print '*'*50+'\nStart qian yi <%s>,shi di <%s> ge zhang hao.'%(oldName,mailnum)
		#判断迁移是否正常.
		if qiyiold(oldServer,oldName,oldPass,newServer,newName,newPass)!=True:
			print '<%s>Failed...'%oldName
			continue
		print '%s ------ %s OK '%(mailnum,oldName)
		#用于替换Yes.记录那个用户的没有迁移过
		tihuanyes(argv[0],mailnum)
	print 'End!!!'

#替换最后一个字段,替换Yes为No
def tihuanyes(*argv):
	try:
		i=0
		fi=open(argv[0],'r')
		fadf=fi.readlines()
		fi.close()
		fi=open(argv[0],'w')
		for fa in fadf:
			i+=1
			if i==argv[1]:
				fa=re.sub(fa.split('\t')[6],'no\n',fa)
			fi.writelines(fa)
		fi.close()
	except Exception,ex:
		print ex

#迁移邮箱的方法
def qiyiold(*argv):
	uid_temp_list=[]
	mailbox_temp=""
	try:
		M=imaplib.IMAP4(argv[0])
		M.login(argv[1],argv[2])
		N=imaplib.IMAP4(argv[3])
		N.login(argv[4],argv[5])
		maildir_l=mail_dir(M.list())
		userNumMail=0
		userAllMail=0
		M.noop()
		N.noop()
		for mailbox in maildir_l:
			userNumMail=int(M.select(mailbox)[1][0])
			userAllMail+=userNumMail
			print '<%s> <%s> <%s>'%(argv[1],mailbox,userNumMail)
		print 'User: <%s> EmailNum: <%s>.'%(argv[1],userAllMail)

		print 'Start qianyi mail....'

		for mailbox in maildir_l:
			# print mailbox
			M.select(mailbox)
			if N.select(mailbox)[0]<>'OK':
				print 'Not mailbox <%s>, Create mailbox <%s>.'%(mailbox,N.create(mailbox)[1])
				N.select(mailbox)
			# N.select(mailbox)
			# 
			# 此步更新于20140813
			old_typ_n,old_data_n=N.search(None,'ALL')
			oldmailid_n=old_data_n[0].split()
			userNumMail=int(M.select(mailbox)[1][0])
			uidlist = panDuanUserBox(argv[0],argv[1],mailbox)
			uid_temp_list=uidlist
			typ,data=M.search(None,'SEEN')
			#print 'seen-------'
			for num in data[0].split():
				# print num
				typ,datauid=M.fetch(num,'UID')
				uid=datauid[0].split(' ')[2][0:-1]
				if(uid in uidlist):
					continue
				else:
					print 'Start downloading...<%s><%s>'%(mailbox,num)
					#实现无痕取信,不影响原来服务器上面邮箱中邮件的状态
					typ,mdata=M.fetch(num,'(UID BODY.PEEK[])')
					print 'download success...'
					print 'Start upload...'
					# print '01'
					if len(mdata[0][1])<1:
						print '<%s> mailbox,num <%s> len=0,continue.'%(mailbox,num)
						continue
					try:
						# print mailbox
						# print '03'
						N.select(mailbox)
					except Exception,ex:
						print '<%s><%s><%s>email error!!!'%(argv[0],mailbox,num)
						N=imaplib.IMAP4(argv[3])
						N.login(argv[4],argv[5])
						N.select(mailbox)
					# print '02'
					try:
						N.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
					except Exception,ex:
						print 'upload error:<%s><%s><%s><%s>'%(argv[1],mailbox,num,ex)
					uidlist.append(uid)
					uid_temp_list=uidlist

			#此步更新于20140813	
			new_typ_n,new_data_n=N.search(None,'ALL')
			newmailid_n=new_data_n[0].split()
			datalist=list(set(oldmailid_n)^set(newmailid_n))
			#

			#typ,data=N.search(None,'ALL')
			# for num in data[0].split():
			for num in datalist:
				N.store(num,'+FLAGS','\SEEN')
			typ,data=M.search(None,'UNSEEN')
			# print 'unseen--------'
			# for num in data[0].split():
				# print num
				# typ,mdata=M.fetch(num,'(UID BODY.PEEK[])')
				# N.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
				
			for num in data[0].split():
				# print num
				typ,datauid=M.fetch(num,'UID')
				uid=datauid[0].split(' ')[2][0:-1]
				if(uid in uidlist):
					continue
				else:
					print 'Start downloading...<%s><%s>'%(mailbox,num)
					typ,mdata=M.fetch(num,'(UID BODY.PEEK[])')
					print 'download success...'
					print 'Start upload...'
					if len(data[0][1])<1:
						print '<%s> mailbox,num <%s> len=0,continue.'%(mailbox,num)
						continue
					try:
						N.select(mailbox)
					except Exception,ex:
						print '<%s><%s><%s>email error!!!'%(argv[0],mailbox,num)
						N=imaplib.IMAP4(argv[3])
						N.login(argv[4],argv[5])
						N.select(mailbox)
					try:
						N.append(mailbox,'',imaplib.Time2Internaldate(time.time()),mdata[0][1])
					except Exception,ex:
						print 'upload error:<%s><%s><%s><%s>'%(argv[1],mailbox,num,ex)
					uidlist.append(uid)
					uid_temp_list=uidlist

			print ('<%s><%s>OK'%(argv[1],mailbox))
			writeuid(argv[0],argv[1],mailbox,uidlist)
			# M.close()
			# N.close()
			# M.logout()
			# N.logout()
		return True
	except Exception,ex:
		print '%s %s'%(argv[1],ex)
		return False
	finally:
		writeuid(argv[0],argv[1],mailbox,uid_temp_list)


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

#计算所有用户总邮件数量
def allmail(*argv):
	allmailnum=0
	userlist=readName(argv[0])
	for user in userlist:
		oldServer=user[0]
		oldName=user[1]
		oldPwd=user[2]
		daoy=re.sub(r'\n','',user[6])
		dao=re.sub(r'\r','',daoy)
		if dao.upper()=='NO':
			print 'Mail account %s does not need to migrate'%oldName
			continue
		try:
			M=imaplib.IMAP4(oldServer)
			M.login(oldName,oldPwd)
			maildir=mail_dir(M.list())
			for mdir in maildir:
				allmailnum += int(M.select(mdir)[1][0])
		except Exception,ex:
			elog='Allmail Error: %s'%ex
			errorUserlog(elog)
	return allmailnum

#用于排列邮件夹列表
def mail_dir(mlist):
    # mail_list=[]
    a=['INBOX']
    # for listone in mlist[1]:
    	# mail_list.append(listone.strip('"').split('"')[-1].strip(' '))
    # print mail_list
    # return mail_list
    return a

#此方法用于读出文件中的数据，传回一个数据列表。
def readName(*argv):
	userlist=[]
	try:
		userl=open(argv[0])
		while True:
			lineuser = userl.readline()
			if len(lineuser.strip())==0:
				break
			#去除"#"号注释行.
			if(lineuser[0]=="#"):
				continue
			#添加叠加邮件列表
			userlist.append(lineuser.split('\t'))
	except IOError:
		#如果有IO问题.则直接退出
		print 'Please Check Filename %s is Exist'%argv[0]
		sys.exit()
	#返回邮件列表
	return userlist

#检测环境,比如之前的检测记录相关.
def detectEnvironment(*argv):
	try:
		if(argv[0])=='status':
			# print argv[0]
			print 'Detect Environment ing....'
			if(os.path.exists(corr_user)):
				print 'Cun Zai!'
				print 'tiao guo not status or del %s and jixu ?'%corr_user
				running=True
				while running:
					guess=int(raw_input('Enter an inteager<1  tiaoguo,0  jixu>: '))
					if guess==0:
						os.remove(default_dir+os.path.sep+corr_user)
						return 0
					elif guess==1:
						return 1
					else:
						print 'NO'
			else:
				return 0
		elif argv[0]=='qianyi':
			# print argv[0]
			print 'Detect Environment ing....'
			if(os.path.exists(corr_user)):
				print 'Cun Zai!'
				print 'tiao guo not status or del %s and jixu ?'%corr_user
				running=True
				while running:
					guess=int(raw_input('Enter an inteager<1  tiaoguo,0  jixu>: '))
					if guess==0:
						os.remove(default_dir+os.path.sep+corr_user)
						return 0
					elif guess==1:
						return 1
					else:
						print 'NO'
			else:
				return 0
		sys.exit()
	except Exception,ex:
		print "Enter Error!!!! %s"%ex


#此方法用于检测服务器,用户名,密码,是否正常
def Status(*argv):
	currnum=0
	erruser=0
	if detectEnvironment(argv[1])==0:
		oldServer_List=[]
		newServer_list=[]
		print 'Check mail username and password,filename is <%s>.' %argv[0]
		for line in readName(argv[0]):
			# print line
			oldServer=line[0]
			oldName=line[1]
			oldPass=line[2]
			newServer=line[3]
			newName=line[4]
			newPass=line[5]
			#由于系统有可能是Linux的.有可能是Windows的,分开做下判断
			ifQianYi=re.sub(r'\n','',line[6])
			ifQianYi=re.sub(r'\r','',ifQianYi)
			line='%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(oldServer,oldName,oldPass,newServer,newName,newPass,ifQianYi)
			#测试oldServer是否是正常的.先判断是否在列表中.
			# print 'OK'
			if oldServer not in oldServer_List:
				if testServer(oldServer):
					oldServer_List.append(oldServer)
				else:
					errorlog='oldServer Error: %s' %oldServer
					errorUserlog(errorlog)
					erruser+=1
					continue
			#测试oldName是否是正常的.
			testOldUser=testUser(oldServer,oldName,oldPass)
			if testOldUser != True:
				errorlog='oldName Logout Failed: %s'%oldName
				errorUserlog(errorlog)
				erruser+=1
				continue
			#测试newServer是否是正常的.先判断是否在列表中
			if newServer not in newServer_list:
				if testServer(newServer):
					newServer_list.append(newServer)
				else:
					errorlog='newServer Error: %s'%newServer
					errorUserlog(errorlog)
					erruser+=1
					continue
			#测试newName是否是正常的.
			testNewUser=testUser(newServer,newName,newPass)
			if testNewUser != True:
				errorlog='newName Logout Failed: %s'%newName
				errorUserlog(errorlog)
				erruser+=1
				continue
			corrUser(line)
			currnum+=1
		print 'Corr_usr <%s> file.Error_User <%s> file. '%(corr_user,error_log)
		print 'Correct User Num: %s. Error User Num: %s. '%(currnum,erruser)
		return currnum,erruser
	else:
		return currnum,erruser

#将测试正常的用户信息写入到正常文件中.
def corrUser(*argv):
	try:
		# tempPath=os.path.dirname(__file__)
		fi=file(default_dir+os.path.sep+corr_user,'a+')
		fi.writelines(argv[0])
	except Exception,ex:
		print ex
	finally:
		fi.close()

#测试用户帐号是否正常
def testUser(*argv):
	M=imaplib.IMAP4(argv[0])
	try:
		M.login(argv[1],argv[2])
		return True
	except Exception,ex:
		return ex
	finally:
		M.logout()

#写入错误日志.
def errorUserlog(elog):
    try:
        dt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #tempPath=os.path.join(os.path.dirname(__file__),'log').replace('\\','/')
        
        # if(os.path.isdir(default_dir)):
        # 	os.makedirs(tempPath)
        logrz = '%s\t%s\n'%(dt,elog)
        fi = file(default_dir+os.path.sep+error_log,'a+')
        fi.writelines(logrz)
    except Exception,ex:
        print ex
	#此处有疑问-------------------

#测试服务器是否正常.
def testServer(*argv):
	try:
		M=imaplib.IMAP4(argv[0])
		M.logout()
		return True
	except Exception,ex:
		return ex

# #帮助方法
# def Help():
# 	filename= __file__
# 	command_text='|>python %s [script][filename=name.txt]'%filename
# 	command_text1='|>python %s status name.txt'%filename
# 	command_text2='|>python %s qianyi name.txt'%filename
# 	command_text3='|>python %s help'%filename
# 	command_text4='END'
# 	# print len(__file__)
# 	print ' '+'-'*25+'HELP'+'-'*25
# 	print '|'+' '*54+'|'
# 	print command_text+((55-len(command_text))*' ')+'|'
# 	print command_text1+((55-len(command_text1))*' ')+'|'
# 	print command_text2+((55-len(command_text2))*' ')+'|'
# 	print command_text3+((55-len(command_text3))*' ')+'|'
# 	print '|'+' '*54+'|'
# 	print ' '+((55-len(command_text4))/2*'-')+command_text4+(((55-len(command_text4))-1)/2*'-')+' '
				
def Help():
	print '''
	 ------------------HELP---------------------------
	|                                                 |
	|>python qyemail.exe [script][filename=name.txt]  |
	|>python qyemail.exe status name.txt              |
	|>python qyemail.exe qianyi name.txt              |
	|>python qyemail.exe help                         |
	|                                                 |
	 ------------------END----------------------------
				'''
if __name__=='__main__':
	Menu()