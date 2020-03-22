from abc import abstractmethod

from django.views.decorators.csrf import csrf_protect

from api.base import AbstractCoreAPI
from api.model_api import ConfigAPI


class GeneralClientAPI(AbstractCoreAPI):
    @abstractmethod
    def grabPageData(self, **kwargs):
        pass

    def getSeason(self):
        # TODO: Check if season is defined in the request. If not, we use current season from config
        return ConfigAPI(self.request).getSeason()
