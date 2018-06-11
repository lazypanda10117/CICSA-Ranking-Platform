import urllib

from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import resolve
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import math

from .models import *

@csrf_exempt
def kickRequest(request, loggedin, rend):
    return (lambda x: rend if math.ceil(x+0.5) else
    (lambda y: redirect('adminPermission') if math.ceil(y+0.5) else redirect('adminIndex'))
    (loggedin*2-1))((loggedin*2-1)*(signed_in(request, 'admin')*2-1))

@csrf_exempt
def signed_in(request, user_type):
    return sessionChecker(request, 'uid', 'utype') and request.session['utype']==user_type;

@csrf_exempt
def loghelper(request, log_type, message):
    log = Log(log_creator=request.session['uid'], log_type=log_type, log_content=message);
    log.save();

@csrf_exempt
def logQueryMaker(model_name, type, **kwargs):
    invalid = {'_state'};
    log = type + ' ' + str(model_name.__name__) + ' - ';
    item_dict = filterDict(getModelObject(model_name, **kwargs).__dict__.items(), invalid);
    for key in item_dict:
        log += str(key) + ': ' + str(item_dict[key]) + ', ';
    return log[:-2];

@csrf_exempt
def generateGETURL(path, argList):
    return path + '?' + ''.join([arg[0] + '=' + arg[1] + '&' for arg in argList.items()])[:-1];

@csrf_exempt
def getViewJSON(action, id):
    return {"action": action, "id": id};

@csrf_exempt
def filterModelObject(model_name, **kwargs):
    result = model_name.objects.filter(**kwargs).all();
    return result;

@csrf_exempt
def getModelObject(model_name, **kwargs):
    try:
        result = model_name.objects.get(**kwargs);
    except:
        result = None;
    return result;

@csrf_exempt
def sessionChecker(request, *args):
    for arg in args:
        if  not (arg in request.session) or request.session[arg] is None:
            return False;
    return True;

@csrf_exempt
def filterDict(dict_items, invalid):
    return {key: val for key, val in dict_items if key not in invalid};

@csrf_exempt
def grabValueAsList(dict):
    return list(dict.values());

@csrf_exempt
def getPostObj(post_dict, name):
    return post_dict[name][0];

@csrf_exempt
def grabLinkValueFromChoices(choices, key):
    return (lambda x: x if x else None)([value[1] for i, value in enumerate(choices) if value[0] == key][0]);

@csrf_exempt
def noneCatcher(key, data):
    return data[key] if key in data else None;

@csrf_exempt
def emptyActionRedirect(request, func):
    #TODO: redirect to action=view
    print(request.GET)
    if request.GET.get('action') is None:
        current_url = resolve(request.path_info).url_name;
        params = 'action=view';
        return HttpResponseRedirect(current_url + "?%s" % params);
    else:
        return func;