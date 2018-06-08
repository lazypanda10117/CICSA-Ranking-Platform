from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import math

from .models import *

@csrf_exempt
def kickRequest(request, loggedin, rend):
    return (lambda x: rend if math.ceil(x+0.5) else (lambda y: redirect('adminPermission') if math.ceil(y+0.5) else redirect('adminIndex')) (loggedin*2-1))((loggedin*2-1)*(signed_in(request)*2-1))

@csrf_exempt
def signed_in(request):
    return True if (request.session.has_key('uid') and request.session['uid']!= None) else False;

@csrf_exempt
def loghelper(request, log_type, message):
    log = Log(log_creator=request.session['uid'], log_type=log_type, log_content=message);
    log.save();

@csrf_exempt
def generateGETURL(path, argList):
    return path + '?' + ''.join([arg[0] + '=' + arg[1] + '&' for arg in argList.items()])[:-1];

@csrf_exempt
def getViewJSON(action, id):
    return {"action": action, "id": id};

def getModelObject(name, field):
    pass;