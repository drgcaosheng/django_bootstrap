from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

def hello(request):
    return render_to_response('index.html',{'system_list':'None'})

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('index.html')

def boots(request):
    return render_to_response('test.html')

def hours_ahead(requst,offset):
    try:
        offset=int(offset)
    except ValueError:
        raise Http404()
    dt=datetime.datetime.now()+datetime.timedelta(hours=offset)
    return render_to_response('index.html',{'now':dt})