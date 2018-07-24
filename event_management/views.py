from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *

from .models import *


def index(request):
    return kickRequest(request, True, render(request, 'console/index.html'));

def dispatch(request, dispatch_path):
    pass;

def dispatchSpecific(request, dispatch_path, element_id):
    pass;