from ..base.GeneralModelAPI import GeneralModelAPI
from misc.CustomFunctions import UrlFunctions
from cicsa_ranking.models import EventActivity


class EventActivityAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return EventActivity

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = self.verifySelf(id=event_activity_id)
        event_activity.event_activity_status = event_activity_status
        event_activity.save()

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = self.verifySelf(id=event_activity_id)
        event_activity.event_activity_result = event_activity_result
        event_activity.save()

    @staticmethod
    def getEventActivityModifyLink(**kwargs):
        return UrlFunctions.getModifyLink('event activity', **kwargs)
