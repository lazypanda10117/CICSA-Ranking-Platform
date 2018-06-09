from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import math
import pdb

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

@csrf_exempt
def getModelObject(model_name, **kwargs):
    #TODO: general function to get model object
    result = model_name.objects.filter(**kwargs).all();
    return result;

@csrf_exempt
def filterDict(dict_items, invalid):
    return {key: val for key, val in dict_items if key not in invalid};

@csrf_exempt
def grabValueAsList(dict):
    return list(dict.values());

@csrf_exempt
def noneCatcher(key, data):
    return data[key] if key in data else None;