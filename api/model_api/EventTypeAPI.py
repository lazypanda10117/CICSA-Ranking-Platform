from cicsa_ranking.models import EventType
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class EventTypeAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventType;