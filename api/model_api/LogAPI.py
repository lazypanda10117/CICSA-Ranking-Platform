from cicsa_ranking.models import Log
from ..base.GeneralModelAPI import GeneralModelAPI


class LogAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Log
