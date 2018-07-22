from .API import *
from ..generalFunctions import *
from ..models import *

class EventAPI(API):
    def __init__(self):
        pass;

    def getEventActivities(self, **kwargs):
        return filterModelObject(EventActivity, **kwargs);

    def getEvent(self, **kwargs):
        return getModelObject(Event, **kwargs);

    def getEvents(self, **kwargs):
        return filterModelObject(Event, **kwargs);

    def getEventTags(self, **kwargs):
        return filterModelObject(EventTag, **kwargs);

    def updateEventStatus(self, event_id, event_status):
        event = getModelObject(Event, id=event_id);
        event.event_status = event_status;
        event.save();
