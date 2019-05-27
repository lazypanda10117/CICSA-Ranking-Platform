from cicsa_ranking.models import School, Event
from api.base.GeneralModelAPI import GeneralModelAPI
from api.model_api import EventAPI


class SchoolAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return School

    def getParticipatedNormalEvents(self, school_id, status=None, season=None):
        if season is None:
            if status is None:
                return EventAPI(self.request).filterSelf(
                    event_school_ids__contains=[school_id]
                ).exclude(event_name__in=Event.EVENT_NAME_FINAL_RACE)
            else:
                return EventAPI(self.request).filterSelf(
                    event_status=Event.EVENT_STATUS_DONE,
                    event_school_ids_contains=[school_id]
                ).exclude(event_name__in=Event.EVENT_NAME_FINAL_RACE)
        else:
            if status is None:
                return EventAPI(self.request).filterSelf(
                    event_season=season,
                    event_school_ids__contains=[school_id]
                ).exclude(event_name__in=Event.EVENT_NAME_FINAL_RACE)
            else:
                return EventAPI(self.request).filterSelf(
                    event_season=season,
                    event_status=Event.EVENT_STATUS_DONE,
                    event_school_ids_contains=[school_id]
                ).exclude(event_name__in=Event.EVENT_NAME_FINAL_RACE)

