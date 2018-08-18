from cicsa_ranking.models import EventTag
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class EventTagAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventTag;