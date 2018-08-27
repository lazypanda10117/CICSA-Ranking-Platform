from cicsa_ranking.models import School
from ..base.GeneralModelAPI import GeneralModelAPI


class SchoolAPI(GeneralModelAPI):
    def setBaseClass(self):
        return School
