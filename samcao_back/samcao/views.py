from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

def hello(request):
    return HttpResponse('Hello World')

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('index.html',{'now':now})

def boots(request):
    return render_to_response('test.html')