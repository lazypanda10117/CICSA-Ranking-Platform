from blackbox.api.base.GeneralModelAPI import GeneralModelAPI
from misc.GeneralFunctions import generalFunctions as gf
from cicsa_ranking.models import EventActivity


class EventActivityAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventActivity;

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = self.auth_class.authenticate('edit', gf.getModelObject(EventActivity, id=event_activity_id));
        gf.raise404Empty(event_activity);
        event_activity.event_activity_status = event_activity_status;
        event_activity.save();

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = self.auth_class.authenticate('edit', gf.getModelObject(EventActivity, id=event_activity_id));
        event_activity.event_activity_result = event_activity_result;
        event_activity.save();

    #the event team links function is to event team

    #the event team function is to team

    def getEventActivityModifyLink(self, **kwargs):
        return gf.getModifiyLink('event activity', **kwargs);