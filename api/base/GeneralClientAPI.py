from abc import abstractmethod

from api.base import AbstractCoreAPI
from api.model_api import ConfigAPI


class GeneralClientAPI(AbstractCoreAPI):
    @abstractmethod
    def grabPageData(self, **kwargs):
        pass

    def getSeason(self):
        # Check if season is defined in the request. If not, we use current season from config
        current_configuration = ConfigAPI(self.request).getAll()[0]
        current_season = current_configuration.config_current_season
        return current_season
