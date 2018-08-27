from ..base.GeneralModelAPI import GeneralModelAPI
from misc.CustomFunctions import ModelFunctions, AuthFunctions, UrlFunctions
from cicsa_ranking.models import EventActivity


class EventActivityAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventActivity

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = self.auth_class.authenticate(
            'edit', ModelFunctions.getModelObject(EventActivity, id=event_activity_id))
        AuthFunctions.raise404Empty(event_activity)
        event_activity.event_activity_status = event_activity_status
        event_activity.save()

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = self.auth_class.authenticate(
            'edit', ModelFunctions.getModelObject(EventActivity, id=event_activity_id))
        AuthFunctions.raise404Empty(event_activity)
        event_activity.event_activity_result = event_activity_result
        event_activity.save()

    # event team links function -> event team

    # event team function -> team

    @staticmethod
    def getEventActivityModifyLink(**kwargs):
        return UrlFunctions.getModifiyLink('event activity', **kwargs)
