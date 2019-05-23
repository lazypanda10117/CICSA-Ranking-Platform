from cicsa_ranking.models import Config, NewsBump, NewsComment, NewsPost
from misc.CustomFunctions import APIFunctions
from api.base import AbstractCoreAPI


class NewsAPI(AbstractCoreAPI):
    def __init__(self, request):
        super().__init__(request)
        self.admin_ids = self.__applyAPI(Config).getAdminIDs()

    # Utility Functions
    def __applyAPI(self, model):
        return APIFunctions.applyModelAPI(model, self.request)

    def __checkAdminPermission(self, action):
        if not self.context.authType == 'admin':
            raise PermissionError("You do not have sufficient permission to perform action {}".format(action))

    # News Functions
    def getRecentNewsPreviews(self, history=5):
        recent_news = self.getRecentNews(history=history)
        for news in recent_news:
            news.news_post_content = (
                lambda content: content[:150] + " ..." if len(content) > 150 else content
            )(news.news_post_content)
        return recent_news

    def getRecentNews(self, history=5):
        recent_news = self.__applyAPI(NewsPost).filterSelf(
            news_post_owner__in=self.admin_ids,
            news_post_status__in=[NewsPost.NEWS_POST_PINNED, NewsPost.NEWS_POST_ACTIVE]
        ).order_by('news_post_status', '-news_post_create_time')[:history]
        print(recent_news)
        return recent_news

    def getNews(self, news_filter=None):
        if news_filter is None:
            return self.__applyAPI(NewsPost).getAll()
        else:
            return self.__applyAPI(NewsPost).filterSelf(**news_filter)

    def getNewsById(self, news_id):
        news = self.getNews(dict(id=news_id))
        return news

    def archiveNews(self, news_id):
        self.__checkAdminPermission('archive news')
        news = self.__applyAPI(NewsPost).verifySelf(id=news_id)
        if news.news_post_status == NewsPost.NEWS_POST_ARCHIVED:
            raise PermissionError("This news is already archived")
        else:
            news.update(news_post_status=NewsPost.NEWS_POST_ARCHIVED)

    def pinNews(self, news_id):
        self.__checkAdminPermission('pin news')
        news = self.__applyAPI(NewsPost).verifySelf(id=news_id)
        if news.news_post_status == NewsPost.NEWS_POST_PINNED:
            raise PermissionError("This news is already pinned")
        else:
            news.update(news_post_status=NewsPost.NEWS_POST_PINNED)

    def restoreNews(self, news_id):
        self.__checkAdminPermission('restore news')
        news = self.__applyAPI(NewsPost).verifySelf(id=news_id)
        if news.news_post_status in [NewsPost.NEWS_POST_ARCHIVED, NewsPost.NEWS_POST_PINNED]:
            news.update(news_post_status=NewsPost.NEWS_POST_ACTIVE)
        else:
            raise PermissionError("This news is not restorable")

    def addNews(self, news_title, news_content):
        self.__checkAdminPermission("add news")
        news = NewsPost()
        news.news_post_title = news_title
        news.news_post_content = news_content
        news.news_post_status = NewsPost.NEWS_POST_ARCHIVED
        news.news_post_owner = self.context.authID
        news = self.__applyAPI(NewsPost).addSelf(news)
        news.save()

    def editNews(self, news_id, news_title, news_content):
        self.__checkAdminPermission("add news")
        news = self.getNews(news_id)
        news.news_post_title = news_title
        news.news_post_content = news_content
        news = self.__applyAPI(NewsPost).verifySelf(news)
        news.save()

    def deleteNews(self, news_id):
        self.__checkAdminPermission("delete news")
        news = self.__applyAPI(NewsPost).deleteSelf(id=news_id)
        news.delete()

    # Comment Functions
    def getComments(self, comment_filter=None):
        if comment_filter is None:
            return self.__applyAPI(NewsComment).getAll()
        else:
            return self.__applyAPI(NewsComment).filterSelf(**comment_filter)

    def getCommentsById(self, news_id):
        comments = self.getComments(dict(news_comment_post_id=news_id))
        return comments

    def replyComment(self, news_id, comment_content):
        comment = NewsComment()
        comment.news_comment_content = comment_content
        comment.news_comment_post_id = news_id
        comment.news_comment_owner = self.context.authID
        comment = self.__applyAPI(NewsComment).addSelf(comment)
        comment.save()

    def deleteComment(self, comment_id):
        self.__checkAdminPermission("delete comment")
        comment = self.__applyAPI(NewsComment).deleteSelf(id=comment_id)
        comment.delete()

    # Bumping Functions
    def canBump(self, news_id):
        if self.context.authType == "public":
            return False
        else:
            return self.hasBumped(news_id)

    def hasBumped(self, news_id):
        bump = self.__applyAPI(NewsBump).getSelf(news_bump_post_id=news_id, news_bump_bumpper_id=self.context.authID)
        return bump is not None

    def bumpNews(self, news_id):
        news = self.__applyAPI(NewsPost).getSelf(id=news_id)
        if news is not None:
            if self.hasBumped(news_id):
                raise PermissionError("You cannot bump a news more than once.")
            else:
                bump = NewsBump()
                bump.news_bump_bumpper_id = self.context.authID
                bump.news_bump_post_id = news_id
                bump.save()
                news.update(news_post_bumps=news.news_post_bumps + 1)
        else:
            raise PermissionError("The news you are bumping does not exist")

    def unbumpNews(self, news_id):
        news = self.__applyAPI(NewsPost).getSelf(id=news_id)
        if news is not None:
            if self.hasBumped(news_id):
                bump = self.__applyAPI(NewsBump).deleteSelf(
                    news_bump_post_id=news_id,
                    news_bump_bumpper_id=self.context.authID
                )
                bump.delete()
                news.update(news_post_bumps=news.news_post_bumps - 1)
            else:
                raise PermissionError("You cannot un-bump a news whe you have not bumped it previously.")

        else:
            raise PermissionError("The news you are un-bumping does not exist")
