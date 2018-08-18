from cicsa_ranking.models import Season
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class SeasonAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Season;