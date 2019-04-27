from django.shortcuts import reverse
from ..base.GeneralClientAPI import GeneralClientAPI
from ..model_api import SeasonAPI


class SeasonPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        def genSeasonTable():
            seasons = SeasonAPI(self.request).getAll().order_by('season_name')
            season_dict = list(map(lambda season: dict(
                season_name=season.season_name,
                season_link='#'
            ), list(seasons)))
            return season_dict

        page_data = dict(
            Seasons=genSeasonTable()
        )
        return page_data
