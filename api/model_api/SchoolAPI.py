from cicsa_ranking.models import School
from ..base.GeneralModelAPI import GeneralModelAPI


class SchoolAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return School
