from cicsa_ranking.models import NewsClap
from ..base.GeneralModelAPI import GeneralModelAPI


class NewsClapAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return NewsClap
