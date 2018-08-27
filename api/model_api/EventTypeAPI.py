from cicsa_ranking.models import EventType
from ..base.GeneralModelAPI import GeneralModelAPI


class EventTypeAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventType
