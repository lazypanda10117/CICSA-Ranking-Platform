from django.conf.urls import url
from django.shortcuts import render, HttpResponse, redirect, reverse

from .models import *
from .forms import *

def index(request):
    return redirect(reverse('eventChoice'));

def choice(request):
    return render(request, 'console/event.html');

def eventAppDispatch(request, event_type):
    dispatch = {'fleet', 'group'};
    return redirect('adminCustomView', event_type) if event_type in dispatch else \
        HttpResponse('Error: Event Type Does Not Exist.');