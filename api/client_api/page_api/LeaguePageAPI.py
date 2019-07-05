from django.urls import reverse

from misc.CustomFunctions import MiscFunctions
from api.base.GeneralClientAPI import GeneralClientAPI
from api.functional_api import NewsAPI
from api.functional_api import LeagueScoringAPI
from api.model_api import AccountAPI
from api.model_api import SchoolAPI


class LeaguePageAPI(GeneralClientAPI):
    def __schoolUrlTransformer(self, school_id):
        return reverse(
            'client.view_dispatch_param',
            args=['school_details', school_id]
        )

    def grabPageData(self, **kwargs):
        def genLeagueTable():
            content = list()
            league_scoring_list = LeagueScoringAPI(self.request).getClientLeagueScoreData()
            sorted_score_list = sorted(
                league_scoring_list, 
                key=lambda league_obj: league_obj.get('display_score'),
                reverse=True
            )
            for idx, league_score in enumerate(sorted_score_list):
                league_row = dict(
                    rank=idx+1,
                    school_id=league_score.get('school_id'),
                    school_name=league_score.get('school_name'),
                    school_url=self.__schoolUrlTransformer(league_score.get('school_id')),
                    num_race=league_score.get('num_race'),
                    league_score=MiscFunctions.truncateDisplayScore(league_score.get('display_score')),
                    score_finalized=league_score.get('compiled'),
                )
                content.append(league_row)
            return content

        page_data = dict(
            scores=genLeagueTable()
        )
        return page_data

