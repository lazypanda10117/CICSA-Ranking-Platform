from cicsa_ranking.models import EventTag
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class EventTagAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return EventTag

    @staticmethod
    def getEventTagModifyLink(**kwargs):
        return UrlFunctions.getModifyLink('event tag', **kwargs)
