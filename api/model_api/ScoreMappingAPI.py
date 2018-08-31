from cicsa_ranking.models import ScoreMapping
from ..base.GeneralModelAPI import GeneralModelAPI


class ScoreMappingAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return ScoreMapping
