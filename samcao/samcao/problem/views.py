# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from samcao.problem.models import System,Type,Way
# import tiqujinyan
import os,sys,time,urllib2,re
import cookielib
import multiprocessing
import datetime,time



def index(request):
    t_list=Type.objects.all()
    w_list=Way.objects.all()
    return render_to_response('index.html',{'typeList':t_list,'wayList':w_list})

def add_way(request):
    t_list=Type.objects.all()
    return render_to_response('add_way.html',{'typeList':t_list})

def jy_list(request):
    # hello=tiqujinyan.sys_input_wap('他二姨的家')
    # return HttpResponse(hello)
    errors=[]
    t_list=Type.objects.all()
    if 'jy_name' in request.GET:
        jy_name=request.GET['jy_name']
        if not jy_name:
            errors.append('Please input ID!!!')
            # return render_to_response('jy_list.html',{'typeList':t_list,'errors':'Error'})
        else:

            url_baidu='http://jingyan.baidu.com/user/npublic/expList?un='

            jy_name=re.sub(r'\n','',jy_name)
            jy_name=re.sub(r'\n','',jy_name)
            # raw_str=urllib2.quote(jy_name)
            url=url_baidu+jy_name
            # return HttpResponse(url)
            # return HttpResponse(url)
            # web=urllib2.urlopen(url).read()
            # return HttpResponse(web)
            return render_to_response('jy_list.html',{'typeList':t_list,'jy_name':url})
    return render_to_response('jy_list.html',{'typeList':t_list,'errors':errors})


def system_gl(request):
    t_list=Type.objects.all()
    return render_to_response('system_gl.html',{'typeList':t_list})
