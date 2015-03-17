# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from samcao.problem.models import System,Type,Way

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
    return render_to_response('add_way.html',{'typeList':t_list})

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
