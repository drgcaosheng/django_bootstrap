# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from samcao.problem.models import System,Type,Way,User
from samcao.problem.forms import OldEmailBox
#POST
from django.template import RequestContext
#testmailbox
import testemail

import tqjinyanends
import cookielib
import datetime,time
import os,sys,time,urllib2,re,urllib
import multiprocessing

def index(request):
    t_list=Type.objects.all()
    w_list=Way.objects.all()
    return render_to_response('index.html',{'typeList':t_list,'wayList':w_list})

def add_way(request):
    t_list=Type.objects.all()
    username=User.objects.filter(user_name='test')[0]
    system_list = System.objects.all()
    return render_to_response('add_way.html',{'typeList':t_list,'username':username,'system_list':system_list})

def jy_list(request):
    errors=[]
    t_list=Type.objects.all()
    if 'jy_name' in request.GET:
        jy_name=request.GET['jy_name']
        if not jy_name:
            errors.append('Please input ID!!!')
        else:
            jy_name=re.sub(r'\n','',jy_name)
            jy_name=re.sub(r'\n','',jy_name)
            jy_name=jy_name.encode('utf-8')
            # print jy_name
            jy_name=urllib2.quote(jy_name)
            web=tqjinyanends.sys_input2(jy_name)
            # print web
            return render_to_response('jy_list.html',{'typeList':t_list,'jy_name':web})
    return render_to_response('jy_list.html',{'typeList':t_list,'errors':errors})

def system_gl(request):
    t_list=Type.objects.all()
    return render_to_response('system_gl.html',{'typeList':t_list})

def test_gl(request):
    t_list=Type.objects.all()
    return render_to_response('test_gl.html',{'typeList':t_list})


def search(request):
    if 'q' in request.GET:
        message = request.GET['q']
    else:
        message = "No"
    return HttpResponse(message)

def qy_email(request):
    t_list=Type.objects.all()
    errors=[]
    if request.method=='POST':
        if not request.REQUEST.get('inputMailServer3',''):
            errors.append('Enter a Mail Server!')
        if not request.REQUEST.get('inputEmail3',''):
            errors.append('Enter a Email Address!')
        if not request.REQUEST.get('inputPassword3',''):
            errors.append('Enter a Password!')
        if request.REQUEST.get('inputEmail3','') and '@' not in request.REQUEST['inputEmail3']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            mailServer = request.POST.get('inputMailServer3','')
            emailAddress = request.POST.get('inputEmail3','')
            passWord = request.POST.get('inputPassword3','')
            ssl = request.POST.get('ssl','')
            #message=mailServer+'|'+emailAddress+'|'+passWord+'|'+ssl
            #print message
            message= testemail.runTestOldMailbox(mailServer,emailAddress,passWord,ssl)
            if str(message).upper()=='TRUE':
                print str(message).upper()
                message='TRUE'
            return render_to_response('qy_email.html',{'typelist':t_list,
													   'message':message,
													   'inputMailServer3':request.REQUEST.get('inputMailServer3',''),
													   'inputEmail3':request.REQUEST.get('inputEmail3',''),
													   'inputPassword3':request.REQUEST.get('inputPassword3',''),
													   'errors':errors
			},context_instance=RequestContext(request))
	    #return render_to_response('qy_email.html',{'typeList':t_list,'newMailServer':message})
    return render_to_response('qy_email.html',{
        'typeList':t_list,
        'inputMailServer3':request.REQUEST.get('inputMailServer3',''),
        'inputEmail3':request.REQUEST.get('inputEmail3',''),
        'inputPassword3':request.REQUEST.get('inputPassword3',''),
        'errors':errors
    },context_instance=RequestContext(request))


def qy_emailtest(request):
    message = request.REQUEST.get('inputMailServer3','')
    return HttpResponse(message)























