import json

from .API import *
from ..generalFunctions import *
from ..models import *

class EventAPI(API):
    def __init__(self, request):
        self.request = request;

    def getEventActivities(self, **kwargs):
        return filterModelObject(EventActivity, **kwargs);

    def getEvent(self, **kwargs):
        return getModelObject(Event, **kwargs);

    def getEvents(self, **kwargs):
        return filterModelObject(Event, **kwargs);

    def getEventTags(self, **kwargs):
        return filterModelObject(EventTag, **kwargs);

    def getEventSummaries(self, **kwargs):
        return filterModelObject(Summary, **kwargs);

    def getEventTeams(self, event_id):
        event_activities = filterModelObject(EventActivity, event_activity_event_parent=event_id);
        event_activity_ids = [activity.id for activity in event_activities];
        event_team_links = filterModelObject(EventTeam, event_team_event_activity_id__in=event_activity_ids).distinct('event_team_id');
        event_team_ids = [team.event_team_id for team in event_team_links];
        event_teams = filterModelObject(Team, id__in=event_team_ids);
        return event_teams;

    def updateEventStatus(self, event_id, event_status):
        event = getModelObject(Event, id=event_id);
        event.event_status = event_status;
        event.save();
        loghelper(self.request, 'admin', logQueryMaker(Event, 'Edit', id=event.id))

    def getEventSummaryModifiyLink(self, **kwargs):
        return getModifiyLink('summary', **kwargs);

    def getEventTagModifyLink(self, **kwargs):
        return getModifiyLink('event tag', **kwargs);

    def getTeamModifyLink(self, **kwargs):
        return getModifiyLink('team', **kwargs);

    def getEventModifyLink(self, **kwargs):
        return getModifiyLink('event', **kwargs);