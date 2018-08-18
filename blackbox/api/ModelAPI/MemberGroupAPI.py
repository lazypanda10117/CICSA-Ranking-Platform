from cicsa_ranking.models import MemberGroup
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class MemberGroupAPI(GeneralModelAPI):
    def setBaseClass(self):
        return MemberGroup;