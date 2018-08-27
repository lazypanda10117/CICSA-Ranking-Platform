from cicsa_ranking.models import ScoreMapping
from ..base.GeneralModelAPI import GeneralModelAPI


class ScoreMappingAPI(GeneralModelAPI):
    def setBaseClass(self):
        return ScoreMapping
