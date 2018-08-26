from cicsa_ranking.models import Team
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class TeamAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Team;

    def getTeamModifyLink(self, **kwargs):
        return UrlFunctions.getModifiyLink('team', **kwargs);
