from cicsa_ranking.models import School, Event
from api.base.GeneralModelAPI import GeneralModelAPI
from api.model_api.EventAPI import EventAPI


class SchoolAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return School

    def getParticipatedEvents(self, school_id, status=None, season=None):
        filter_kwargs = dict(
            event_school_ids__contains=[school_id]
        )
        if status is not None:
            filter_kwargs["event_status"] = status
        if season is not None:
            filter_kwargs["event_season"] = season

        return EventAPI(self.request).filterSelf(**filter_kwargs)

    def getParticipatedNormalEvents(self, school_id, status=None, season=None):
        return self.getParticipatedEvents(
            school_id, status, season
        ).exclude(event_name__in=Event.EVENT_NAME_FINAL_RACE)
