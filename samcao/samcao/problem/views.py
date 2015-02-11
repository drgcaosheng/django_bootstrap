from django.shortcuts import render_to_response
from samcao.problem.models import System

def returnSystemList(request):
    s_list=System.objects.all()
    return render_to_response('index.html',{'system_list':s_list})

def system_gl(request):
    return render_to_response('index.html',{'system_list':s_list})