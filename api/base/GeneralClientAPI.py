from abc import abstractmethod
from api.base import AbstractCoreAPI


class GeneralClientAPI(AbstractCoreAPI):
    @abstractmethod
    def grabPageData(self, **kwargs):
        pass
