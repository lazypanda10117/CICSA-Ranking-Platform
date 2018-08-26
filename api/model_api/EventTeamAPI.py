from cicsa_ranking.models import EventTeam
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class EventTeamAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventTeam;

    @staticmethod
    def getEventTeamModifyLink(self, **kwargs):
        return UrlFunctions.getModifiyLink('event team', **kwargs);