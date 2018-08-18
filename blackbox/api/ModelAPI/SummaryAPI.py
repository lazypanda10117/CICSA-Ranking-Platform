from cicsa_ranking.models import Summary
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class SummaryAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Summary;