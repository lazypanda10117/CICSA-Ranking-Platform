from django.urls import reverse

from cicsa_ranking.models import NewsPost
from api.base.GeneralClientAPI import GeneralClientAPI
from api.functional_api import NewsAPI
from api.model_api import AccountAPI


class LeaguePageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genLeagueTable(season_id):
            if season_id is None:
                pass
            else:
                news_partition = NewsAPI(self.request).getNews(
                    dict(news_post_status=news_status)
                    ).order_by('-news_post_create_time')
                league_dict = list(map(lambda news: dict(
                    news_post_link=reverse("client.view_dispatch_param", args=["specific_news", news.id]),
                    news_post_title=news.news_post_title,
                    news_post_content=news.news_post_content,
                    news_post_owner_name=AccountAPI(self.request).getAssociatedNameById(news.news_post_owner),
                    news_post_create_time=news.news_post_create_time,
                    news_post_bumps=news.news_post_bumps
                ), list(news_partition)))
            return league_dict

        season_id = kwargs.get(id)
        page_data = dict(
            scores=genLeagueTable(season_id)
        )
        return page_data

