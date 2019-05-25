from cicsa_ranking.models import NewsComment
from ..base.GeneralModelAPI import GeneralModelAPI


class NewsCommentAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return NewsComment
