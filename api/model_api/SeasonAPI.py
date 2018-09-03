from cicsa_ranking.models import Season
from ..base.GeneralModelAPI import GeneralModelAPI


class SeasonAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Season
