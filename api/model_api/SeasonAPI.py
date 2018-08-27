from cicsa_ranking.models import Season
from ..base.GeneralModelAPI import GeneralModelAPI


class SeasonAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Season
