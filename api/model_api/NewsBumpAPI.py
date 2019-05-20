from cicsa_ranking.models import NewsBump
from ..base.GeneralModelAPI import GeneralModelAPI


class NewsBumpAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return NewsBump
