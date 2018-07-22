from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from admin_console.generalFunctions import *
from admin_console.HelperClass import *
from admin_console.API import *

from .models import *


def index(request):
    return kickRequest(request, True, render(request, 'console/index.html'));

def specificEvent(request, event_id):
    return kickRequest(request, True, render(
        request, 'management/displayList.html',
        {'title': 'Event Activities List', 'event_activity_list': genEventActivityList(event_id)}));
    pass;

def specificEventActivity(request, event_activity_id):
    event_api = EventAPI();
    event_activity_api = EventActivityAPI();
    event_activity = event_activity_api.getEventActivity(id=int(event_activity_id));
    event = event_api.getEvent(id=int(event_activity.event_activity_event_parent));
    event_rotation = event.event_rotation_detail;
    event_team_number = event.event_team_number;
    event_activity_order = event_activity.event_activity_order;
    print(event_rotation);
    return kickRequest(request, True, render(
        request, 'management/eventactivityrace.html',
        {'block_title': 'Event Activity Ranking',
         'action_destination': genEventList(),
         'form_id': "test",
         'contents': dict()}));

def eventList(request):
    return kickRequest(request, True, render(
        request, 'management/displayList.html',
        {'title': 'Events List', 'event_list': genEventList()}));

def genEventList():
    def genDict(state):
        events = event_api.getEvents(event_status=state);
        change_status_dict = dict(future='running', running='done', done='not applicable');
        event_dict = map(lambda event: dict(
            event_text=event.event_name,
            event_status_text=change_status_dict[event.event_status],
            event_link=reverse('managementSpecificEvent', args=[event.id]),
            event_status_link=reverse(
                'managementUpdateEventStatus', args=[
                    event.id, change_status_dict[event.event_status]]) if event.event_status != 'done' else '#'),
                         [event for event in events]);
        return dict(block_title=state, contents=event_dict);
    event_api = EventAPI();
    return dict(future=genDict('future'), running=genDict('running'), done=genDict('done'));

def eventActivityList(request, event_id):
    return kickRequest(request, True, render(
        request, 'management/displayList.html',
        {'title': 'Event Activities List', 'event_activity_list': genEventActivityList(event_id)}));

def genEventActivityList(event_id):
    def genDict(event_tag):
        event_activities = event_api.getEventActivities(
            event_activity_event_parent=event_id, event_activity_event_tag=event_tag.id);
        event_dict = map(lambda event_activity: dict(
            event_activity_text=event_activity.event_activity_name,
            event_activity_link=reverse('managementSpecificEventActivity', args=[event_activity.id]),
            event_activity_status=event_activity.event_activity_status),
                         [eventActivity for eventActivity in event_activities]);
        return dict(block_title=event_tag.event_tag_name, contents=event_dict);
    event_api = EventAPI();
    event_tags = event_api.getEventTags(event_tag_event_id=event_id);
    return {event_tag.event_tag_name: genDict(event_tag) for event_tag in event_tags};

def updateEventStatus(request, event_id, event_status):
    if signed_in(request, 'admin'):
        event_api = EventAPI();
        event_api.updateEventStatus(int(event_id), event_status);
    return redirect('managementEvents');
