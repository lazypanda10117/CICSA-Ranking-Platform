from cicsa_ranking.models import EventTeam
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class EventTeamAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return EventTeam

    @staticmethod
    def getEventTeamModifyLink(**kwargs):
        return UrlFunctions.getModifyLink('event team', **kwargs) + '&base=event_mgmt'
