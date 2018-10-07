from abc import abstractmethod
from ..base.AbstractAPI import AbstractAPI


class GeneralClientAPI(AbstractAPI):
    @abstractmethod
    def grabPageData(self, **kwargs):
        pass
