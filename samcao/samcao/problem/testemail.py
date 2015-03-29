#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: testemail.py

import sys
import os
import imaplib
import time
import re
import cPickle as p

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
		if mLogin[0]=='OK':
			testMailServer.logout()
			return True
	except Exception,ex:
		return ex




