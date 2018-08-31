from cicsa_ranking.models import EventType
from ..base.GeneralModelAPI import GeneralModelAPI


class EventTypeAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return EventType
