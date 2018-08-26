from cicsa_ranking.models import Summary
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class SummaryAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Summary;

    @staticmethod
    def getEventSummaryModifiyLink(**kwargs):
        return UrlFunctions.getModifiyLink('summary', **kwargs);