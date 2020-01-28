from cicsa_ranking.models import EventActivity
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class EventActivityAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return EventActivity

    def updateEventActivityState(self, event_activity_id, event_activity_status):
        event_activity = self.editSelf(id=event_activity_id)
        event_activity.event_activity_status = event_activity_status
        event_activity.save()

    def updateEventActivityResult(self, event_activity_id, event_activity_result):
        event_activity = self.editSelf(id=event_activity_id)
        event_activity.event_activity_result = event_activity_result
        event_activity.save()

    def addEventActivity(self, event_id):
        pass

    def deleteEventActivity(self, event_activity_id):
        pass

    @staticmethod
    def getEventActivityModifyLink(**kwargs):
        return UrlFunctions.getModifyLink('event activity', **kwargs) + '&base=event_mgmt'
