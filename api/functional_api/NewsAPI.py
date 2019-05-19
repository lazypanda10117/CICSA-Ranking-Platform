import json
from django.http import HttpResponse
from ..base.AbstractAPI import AbstractAPI


class NewsAPI(AbstractAPI):
    def getRecentNewsPreviews(self):
        pass

    def getRecentNews(self, size=5):
        pass

    def getNews(self):
        pass

    def archiveNews(self):
        pass

    def addNews(self):
        pass

    def deleteNews(self):
        pass

    def getComments(self):
        pass

    def addComment(self):
        pass

    def replyComment(self):
        pass

    pass
