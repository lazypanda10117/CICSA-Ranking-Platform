from cicsa_ranking.models import Team
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class TeamAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Team;