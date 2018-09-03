from cicsa_ranking.models import Region
from ..base.GeneralModelAPI import GeneralModelAPI


class RegionAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Region
