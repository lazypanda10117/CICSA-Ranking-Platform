from cicsa_ranking.models import Log
from ..base.GeneralModelAPI import GeneralModelAPI


class LogAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Log
