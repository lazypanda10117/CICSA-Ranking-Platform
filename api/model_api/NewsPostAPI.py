from cicsa_ranking.models import NewsPostAPI
from ..base.GeneralModelAPI import GeneralModelAPI


class NewsPostAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return NewsPostAPI
