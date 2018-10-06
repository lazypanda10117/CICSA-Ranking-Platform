from abc import abstractmethod
from ..base.AbstractAPI import AbstractAPI


class GeneralClientAPI(AbstractAPI):
    def __init__(self, request):
        super().__init__(request)

    @abstractmethod
    def grabPageData(self, **kwargs):
        pass
