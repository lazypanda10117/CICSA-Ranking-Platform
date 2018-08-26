from cicsa_ranking.models import School
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class SchoolAPI(GeneralModelAPI):
    def setBaseClass(self):
        return School;