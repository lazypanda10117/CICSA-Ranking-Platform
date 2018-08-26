from cicsa_ranking.models import Region
from ..base.GeneralModelAPI import GeneralModelAPI


class RegionAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Region;