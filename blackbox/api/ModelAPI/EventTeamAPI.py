from cicsa_ranking.models import EventTeam
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class EventTeamAPI(GeneralModelAPI):
    def setBaseClass(self):
        return EventTeam;