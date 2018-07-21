from .API import *
from ..generalFunctions import *
from ..models import *

class EventAPI(API):
    def __init__(self):
        pass;

    def getEventActivities(self, event):
        pass;

    def getEvent(self):
        pass;

    def getEvents(self, **kwargs):
        return filterModelObject(Event, **kwargs);

    def deleteEvent(self):
        pass;

    def updateRotationDetail(self):
        pass;

    def updateEventRaceNumber(self):
        pass;
