from cicsa_ranking.models import Team
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class TeamAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Team

    @staticmethod
    def getTeamModifyLink(**kwargs):
        return UrlFunctions.getModifyLink('team', **kwargs)
