import json
from django.http import HttpResponse
from api.base.AbstractAPI import AbstractAPI
# from api.model_api import ConfigAPI
# from api.model_api import NewsPostAPI
# from api.model_api import NewsCommentAPI
# from api.model_api import NewsClapAPI
from cicsa_ranking.models import Config, NewsClap, NewsComment, NewsPost
from misc.CustomFunctions import APIFunctions

class NewsAPI(AbstractAPI):
    def __init__(self, request):
        super().__init__(request)
        self.admin_ids = self.__applyAPI(Config).getAdminIDs()

    def __applyAPI(self, model):
        return APIFunctions.applyModelAPI(model, self.request)

    def getRecentNewsPreviews(self, history=5):
        recent_news = self.getRecentNews(history=history)
        for news in recent_news:
            news.news_post_content = (
                lambda content: content[:150] + " ..." if len(content) > 150 else content
            )(news.news_post_content)
        return recent_news

    # TODO: get all the pinned first, then get the active until it reaches limit
    def getRecentNews(self, history=5):
        recent_news = self.__applyAPI(NewsPost).filterSelf(
            news_post_owner__in=self.admin_ids, news_post_status__in=['pinned', 'active'])[:history]
        print(recent_news)
        return recent_news

    def getAllNews(self, news_filter=None):
        if news_filter is None:
            all_news = self.__applyAPI(NewsPost).getAll()
        else
            all_news = self.__applyAPI(NewsPost).filterSelf(news_post_status=news_filter)
        return all_news

    def getNews(self, news_id):
        news = self.__applyAPI(NewsPost).getSelf(id=news_id)
        return news

    def archiveNews(self, news_id):
        news = self.__applyAPI(NewsPost).verifySelf(id=news_id)
        if news.news_post_status == 'archived':
            raise PermissionError("This news is already archived")
        else
            news.news_post_status = 'archived'
            news.save()

    def addNews(self):
        news =
        pass

    def deleteNews(self):
        pass

    def getComments(self):
        pass

    def deleteComment(self):
        pass

    def replyComment(self):
        pass

    def clapNews(self):
        pass

    def unclapNews(self):
        pass
