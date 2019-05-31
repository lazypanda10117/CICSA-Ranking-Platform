from cicsa_ranking.models import Score
from api.base.GeneralModelAPI import GeneralModelAPI

class ScoreAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Score