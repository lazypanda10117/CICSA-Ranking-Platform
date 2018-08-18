from cicsa_ranking.models import Member
from misc.GeneralFunctions import generalFunctions as gf
from blackbox.api.base.GeneralModelAPI import GeneralModelAPI


class MemberAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Member;