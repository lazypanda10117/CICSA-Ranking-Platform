from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *

from .CustomClasses import *
from .models import *

def index(request):
    return redirect(reverse('eventManagementChoice'));

def choice(request):
    types = [value.event_type_name for value in filterModelObject(EventType)];
    type_style = {'width': int(12/len(types)) if len(types) else None}
    return kickRequest(request, True, render(request, 'console/event.html', {'types': types, 'type_style': type_style}));

def eventFilter(request, type):
    return redirect(reverse('eventManagementDispatch', args=['event', type]));

def viewDispatch(request, dispatch_path, param):
    def setDispatcher():
        dispatcher = Dispatcher();
        dispatcher.add('event', EventDisplay);
        dispatcher.add('activity', EventActivityDisplay);
        dispatcher.add('activity detail', EventActivityDetailDisplay);
        return dispatcher;
    dispatcher = setDispatcher();
    object = dispatcher.get(dispatch_path)(request, param);
    return object.render();
