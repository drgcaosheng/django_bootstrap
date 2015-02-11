from django.shortcuts import render_to_response
from samcao.problem.models import System,Type,Way

def returnSystemList(request):
    s_list=System.objects.all()
    return render_to_response('index.html',{'system_list':s_list})

def system_gl(request):
    return render_to_response('index.html',{'system_list':s_list})

def index(request):
    t_list=Type.objects.all()
    w_list=Way.objects.all()
    return render_to_response('type_list.html',{'typeList':t_list,'wayList':w_list})

