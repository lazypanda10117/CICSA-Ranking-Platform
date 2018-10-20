from django.shortcuts import reverse
from ..base.GeneralClientAPI import GeneralClientAPI
from ..functional_api import NewsAPI


class NewsPageAPI(GeneralClientAPI):
    def grabPageData(self, **kwargs):
        page_data = dict()
        return page_data


