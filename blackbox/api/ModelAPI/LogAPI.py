from cicsa_ranking.models import Log
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class LogAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Log;