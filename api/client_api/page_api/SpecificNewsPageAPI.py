from api.base.GeneralClientAPI import GeneralClientAPI
from api.functional_api import NewsAPI
from api.model_api import AccountAPI


class SpecificNewsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genComments(news_id):
            comments = news_api.getCommentsById(news_id).order_by("-news_comment_create_time")
            comments_info = list(map(lambda comment: dict(
                news_comment_owner=comment.news_comment_owner,
                news_comment_owner_name=AccountAPI(self.request).getAssociatedNameById(comment.news_comment_owner),
                news_comment_content=comment.news_comment_content,
                news_comment_create_time=comment.news_comment_create_time
            ), list(comments)))
            return comments_info

        def genNewsTable(news_id):
            news = news_api.getNewsById(news_id)
            specific_news_info = list(map(lambda news: dict(
                news_id=news.id,
                news_post_title=news.news_post_title,
                news_post_content=news.news_post_content,
                news_post_owner=news.news_post_owner,
                news_post_owner_name=AccountAPI(self.request).getAssociatedNameById(news.news_post_owner),
                news_post_create_time=news.news_post_create_time,
                news_post_bumps=news.news_post_bumps,
                news_post_can_bump=news_api.canBump(news_id),
                comments=genComments(news_id)
            ), list(news)))
            return specific_news_info

        news_id = kwargs.get("id")
        news_api = NewsAPI(self.request)
        page_data = dict(
            authenticated=self.context.authType in ["admin", "team"],
            specific_news=genNewsTable(news_id)
        )
        return page_data

