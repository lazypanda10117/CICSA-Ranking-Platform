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
        {'title': 'Events List', 'event_list': genEventList()}));

def genDict(state):
    events = EventAPI().getEvents(event_status=state);
    event_dict = map(lambda event: dict(
        event_text=event.event_name,
        event_status_text=event.event_status,
        event_link=event.event_name,
        event_status_link=event.event_status),
                     [event for event in events]);
    return dict(block_title=state, contents=event_dict);

def genEventList():
    return dict(future=genDict('future'), done=genDict('done'), past=genDict('past'));