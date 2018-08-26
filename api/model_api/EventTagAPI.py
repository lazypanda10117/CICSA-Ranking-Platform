from cicsa_ranking.models import EventTag
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class EventTagAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventTag;

    @staticmethod
    def getEventTagModifyLink(self, **kwargs):
        return UrlFunctions.getModifiyLink('event tag', **kwargs);
