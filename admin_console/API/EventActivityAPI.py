from .API import *
from ..generalFunctions import *
from ..models import *

class EventActivityAPI(API):
    def __init__(self):
        pass;

    def getEventActivity(self, **kwargs):
        return getModelObject(EventActivity, **kwargs);

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = getModelObject(EventActivity, id=event_activity_id);
        event_activity.event_activity_status = event_activity_status;
        event_activity.save();

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = getModelObject(EventActivity, id=event_activity_id);
        event_activity.event_activity_result = event_activity_result;
        event_activity.save();