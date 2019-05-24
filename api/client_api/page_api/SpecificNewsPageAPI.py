from django.shortcuts import reverse
from cicsa_ranking.models import NewsPost
from api.base.GeneralClientAPI import GeneralClientAPI
from api.functional_api import NewsAPI


class SpecificNewsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genNewsTable(news_status):
            news_partition = NewsAPI(self.request).getNews(
                dict(news_post_status=news_status)
                ).order_by('-news_post_create_time')
            news_dict = list(map(lambda news: dict(
                news_post_title=news.news_post_title,
                news_post_content=news.news_post_content,
                news_post_owner=news.news_post_owner,
                news_post_create_time=news.news_post_create_time,
                news_post_bumps=news.news_post_bumps
            ), list(news_partition)))
            return news_dict
        page_data =  dict(
            Pinned=genNewsTable(NewsPost.NEWS_POST_PINNED),
            Active=genNewsTable(NewsPost.NEWS_POST_ACTIVE),
            Archived=genNewsTable(NewsPost.NEWS_POST_ARCHIVED)
            )
        print(page_data)
        return page_data

