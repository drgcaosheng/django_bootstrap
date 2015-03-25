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
    return argv