from cicsa_ranking.models import ScoreMapping
from ..base.GeneralModelAPI import GeneralModelAPI


class ScoreMappingAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return ScoreMapping

    def getMaxSentinel(self):
        return self.base.SCORE_SENTINEL
