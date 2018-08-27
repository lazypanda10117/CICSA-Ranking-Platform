from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .generalFunctions import *
from .HelperClass import *
from .API import *
from .GeneralView import *
from .CustomView import *

from .models import *
from .forms import *

@csrf_exempt
def index(request):
    return kickRequest(request, True, render(request, 'console/index.html'));

@csrf_exempt
def permission(request):
    return kickRequest(request, False, render(request, 'console/login.html'));

@csrf_exempt
def login(request):
    return Authentication(request).login();

@csrf_exempt
def logout(request):
    return Authentication(request).logout();

@csrf_exempt
def search(request):
    item = request.GET.get("item");
    key = request.GET.get("key");
    term = request.GET.get("term");
    return SearchAPI().search(item, key, term);

@csrf_exempt
def generalView(request, form_path):
    return GeneralView(request).dispatch(form_path);

@csrf_exempt
def customView(request, form_path):
    return CustomView(request).dispatch(form_path);
