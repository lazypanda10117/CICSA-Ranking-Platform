from cicsa_ranking.models import Region
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class RegionAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Region;