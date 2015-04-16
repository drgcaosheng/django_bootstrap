# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from samcao.problem.models import System,Type,Way,User
from samcao.problem.forms import OldEmailBox
#POST
from django.template import RequestContext
#testmailbox
import testemail
import pyrules

import tqjinyanends
import cookielib
import datetime,time
import os,sys,time,urllib2,re,urllib
import multiprocessing
import os

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
    olderrors=[]
    newerrors=[]
    oldmessage=[]
    newmessage=[]
    allmessage=''
    if request.method=='POST':
        if not request.REQUEST.get('inputoldmailserver',''):
            olderrors.append('Enter a Mail Server!')
        if not request.REQUEST.get('inputoldemail',''):
            olderrors.append('Enter a Email Address!')
        if not request.REQUEST.get('inputoldpassword',''):
            olderrors.append('Enter a Password!')
        if request.REQUEST.get('inputoldemail','') and '@' not in request.REQUEST['inputoldemail']:
            olderrors.append('Enter a valid e-mail address.')

        if not request.REQUEST.get('inputnewmailserver',''):
            newerrors.append('Enter a Mail Server!')
        if not request.REQUEST.get('inputnewemail',''):
            newerrors.append('Enter a Email Address!')
        if not request.REQUEST.get('inputnewpassword',''):
            newerrors.append('Enter a Password!')
        if request.REQUEST.get('inputnewemail','') and '@' not in request.REQUEST['inputnewemail']:
            newerrors.append('Enter a valid e-mail address.')

        if not olderrors and not newerrors:
            oldmailServer = request.POST.get('inputoldmailserver','')
            oldemailAddress = request.POST.get('inputoldemail','')
            oldpassWord = request.POST.get('inputoldpassword','')
            oldssl = request.POST.get('oldssl','')

            newmailServer = request.POST.get('inputnewmailserver','')
            newemailAddress = request.POST.get('inputnewemail','')
            newpassWord = request.POST.get('inputnewpassword','')
            newssl = request.POST.get('newssl','')
            # print olderrors
            # print newerrors
            csoldEmail=str(testemail.runTestOldMailbox(oldmailServer,oldemailAddress,oldpassWord,oldssl))
            csnewEmail=str(testemail.runTestOldMailbox(newmailServer,newemailAddress,newpassWord,newssl))
            # print csoldEmail
            if csoldEmail.upper()=='TRUE' and csnewEmail.upper()=='TRUE':
                if oldmailServer==newmailServer and oldemailAddress==newemailAddress:
                    allmessage="Old email address is the same with the new email address !!!"
                else:
                    te=oldmailServer+"-"+oldemailAddress+"-"+oldpassWord
                    qy_email=testemail.qiyiold(oldmailServer,oldemailAddress,oldpassWord,oldssl,newmailServer,newemailAddress,newpassWord,newssl)
                    qy_email=str(qy_email).upper()
                    return render_to_response('qdqyemail.html',{'qy_email':qy_email,'oldemailAddress':oldemailAddress,'newemailAddress':newemailAddress})
            else:
                newerrors.append(csnewEmail)
                olderrors.append(csoldEmail)
    return render_to_response('qy_email.html',{
        'typeList':t_list,
        'inputoldmailserver':request.REQUEST.get('inputoldmailserver',''),
        'inputoldemail':request.REQUEST.get('inputoldemail',''),
        'inputoldpassword':request.REQUEST.get('inputoldpassword',''),
		'inputnewmailserver':request.REQUEST.get('inputnewmailserver',''),
		'inputnewemail':request.REQUEST.get('inputnewemail',''),
		'inputnewpassword':request.REQUEST.get('inputnewpassword',''),
        'allmessage':allmessage,
        'oldmessage':oldmessage,
        'newmessage':newmessage,
		'olderrors':olderrors,
        'newerrors':newerrors
    },context_instance=RequestContext(request))


def qy_emailtest(request):
    message = request.REQUEST.get('inputMailServer3','')
    return HttpResponse(message)

def chinese_rules(request):
    cr=pyrules.createRules()
    rulist=cr.returnRulesList()
    errormessage=[]
    searchList=[]
    sear_yes=[]
    selectType=request.REQUEST.get('rulesType','').lower()
    print selectType
    if request.method=='POST':
        if not request.REQUEST.get('exampleInputkeyword',''):
            errormessage.append('Please Input Key Word!!!')
        if not request.REQUEST.get('exampleInputNumber',''):
            errormessage.append('Please Input Key Number!!!')
        if not errormessage:
            searchList=cr.searchRules(request.REQUEST.get('rulesType',''),request.REQUEST.get('exampleInputkeyword',''),request.REQUEST.get('exampleInputNumber',''))
            if not searchList:
                sear_yes.append('yes')

    # print request.REQUEST.get('rulesType','')
    return render_to_response('chinese_rules.html',{
        'rulist':rulist,
        'errormessage':errormessage,
        'exampleInputkeyword':request.REQUEST.get('exampleInputkeyword',''),
        'exampleInputNumber':request.REQUEST.get('exampleInputNumber',''),
        'searchlist':searchList,
        'selectType':selectType,
        'sear_yes':sear_yes
    },context_instance=RequestContext(request))





















