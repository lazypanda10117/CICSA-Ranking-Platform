from cicsa_ranking.models import Season
from api.base import AbstractRequestAPI
from api.model_api import ConfigAPI
from misc.CustomFunctions import MiscFunctions


class SeasonBasedAPI(AbstractRequestAPI):
    def __init__(self, request, season=None, **kwargs):
        super().__init__(request)
        self.all_season = False
        self.season = season
        self.setSeasons(season)

    def setSeasons(self, season):
        # TODO: Check if season is defined in the request. If not, we use current season from config
        self.all_season = (season == Season.ALL_SEASON)
        self.season = MiscFunctions.fallback(season, ConfigAPI(self.request).getSeason())
