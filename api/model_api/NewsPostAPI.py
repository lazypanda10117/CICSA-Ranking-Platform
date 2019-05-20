from cicsa_ranking.models import NewsPost
from ..base.GeneralModelAPI import GeneralModelAPI


class NewsPostAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return NewsPost
