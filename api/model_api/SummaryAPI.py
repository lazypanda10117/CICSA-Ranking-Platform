from cicsa_ranking.models import Summary
from misc.CustomFunctions import UrlFunctions
from ..base.GeneralModelAPI import GeneralModelAPI


class SummaryAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Summary

    @staticmethod
    def getEventSummaryModifiyLink(**kwargs):
        return UrlFunctions.getModifyLink('summary', **kwargs) + '&base=event_mgmt'
