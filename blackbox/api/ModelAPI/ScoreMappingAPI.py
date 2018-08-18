from cicsa_ranking.models import ScoreMapping
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class ScoreMappingAPI(GeneralModelAPI):
    def setBaseClass(self):
        return ScoreMapping;