# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from samcao.problem.models import System,Type,Way,User
from samcao.problem.forms import OldEmailBox
#POST
from django.template import RequestContext
from django.http import StreamingHttpResponse
#testmailbox
import testemail
import pyrules

import csv

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
    errormessage=[]
    selectType=request.REQUEST.get('rulesType','').lower()
    actionType=request.REQUEST.get('actionType','').lower()
    keyWord=request.REQUEST.get('exampleInputkeyword','')
    numberW=request.REQUEST.get('exampleInputNumber','')
    returnlist=[]
    # print actionType
    # print selectType
    if request.method=='POST':
        if not request.REQUEST.get('exampleInputkeyword',''):
            errormessage.append('Please Input Key Word!!!')
        if not request.REQUEST.get('exampleInputNumber',''):
            errormessage.append('Please Input Key Number!!!')
        if not errormessage:
            if 'search' in actionType:
                print actionType
                cr=pyrules.createRules()
                returnlist=cr.searchRules(actionType,selectType,keyWord,numberW)
            elif 'delete' in actionType:
                cr=pyrules.createRules()
                delReturn=cr.delRules(actionType,selectType,keyWord,numberW)
                if delReturn:
                    cr=pyrules.createRules()
                    returnlist=cr.readTq()
                else:
                    returnlist=False
            elif 'update' in actionType:
                cr=pyrules.createRules()
                updateReturn=cr.updateRules(actionType,selectType,keyWord,numberW)
                if updateReturn:
                    cr=pyrules.createRules()
                    returnlist=cr.readTq()
                else:
                    returnlist=False
            elif 'add' in actionType:
                cr=pyrules.createRules()
                addRules=cr.addRules(actionType,selectType,keyWord,numberW)
                if addRules:
                    cr=pyrules.createRules()
                    returnlist=cr.readTq()
                else:
                    returnlist=False
        else:
            print 'not errormessage'
            cr=pyrules.createRules()
            returnlist=cr.readTq()
    else:
        print 'not __  post'
        cr=pyrules.createRules()
        returnlist=cr.readTq()
        # print 'not post'

    return render_to_response('chinese_rules.html',{
        'returnlist':returnlist,
        'errormessage':errormessage,
        'selectType':selectType,
        'actionType':actionType,
        'exampleInputkeyword':request.REQUEST.get('exampleInputkeyword',''),
        'exampleInputNumber':request.REQUEST.get('exampleInputNumber','')
    },context_instance=RequestContext(request))




def readFile(fn, buf_size=262144):
    f=open(fn,"rb")
    while True:
        c=f.read(buf_size)
        if c:
            yield c
        else:
            break
        f.close()


def testtxt(request):
    cr=pyrules.createRules()
    cr.menuCreateDown()
    def file_iterator(file_name,chunk_size=512):
        with open(file_name) as f:
            while True:
                c=f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name=r'rules/chinese_rules.cf'
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def testb(request):
    the_file_name=r'rules/chinese_rules.cf'
    f=file(the_file_name,'r')
    b=f.readlines()
    print b
    return render_to_response('testb.html',{'b':b})


def webmail(request):
    return  render_to_response('webmail_index.html')


def testimage(request):
    image_data=open(r'rules/1.jpg','rb').read()
    return HttpResponse(image_data,mimetype='image/jpg')






