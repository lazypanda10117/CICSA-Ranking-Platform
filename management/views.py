from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *

from .models import *


@csrf_exempt
def index(request):
    return kickRequest(request, True, render(request, 'console/index.html'));

@csrf_exempt
def eventList(request):
    return kickRequest(request, True, render(
        request, 'management/displayList.html',
        {'title': 'Events List', 'event_list': {'future': "hi"}}));

def genDict(request, state):
    event_api = EventAPI();
    events = map(lambda x: x.event_name, [e for e in event_api.getEvents(event_status=state)]);
    return dict(state=dict(block_title=state, contents=events));