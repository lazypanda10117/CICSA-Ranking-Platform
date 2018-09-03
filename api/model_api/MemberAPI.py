from cicsa_ranking.models import Member
from ..base.GeneralModelAPI import GeneralModelAPI


class MemberAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Member
