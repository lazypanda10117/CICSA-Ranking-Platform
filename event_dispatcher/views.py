from django.conf.urls import url
from django.shortcuts import render, HttpResponse, redirect, reverse
from admin_console.generalFunctions import *;
from .models import *


def index(request):
    return redirect(reverse('eventChoice'));

def choice(request):
    types = [value.event_type_name for value in filterModelObject(EventType)];
    type_style = {'width': int(12/len(types)) if len(types) else None}
    return kickRequest(request, True, render(request, 'console/event.html', {'types': types, 'type_style': type_style}));

def eventAppDispatch(request, event_type):
    dispatch = [value.event_type_name for value in filterModelObject(EventType)];
    return redirect('adminCustomView', event_type) if event_type in dispatch else \
        HttpResponse('Error: Event Type Does Not Exist.');