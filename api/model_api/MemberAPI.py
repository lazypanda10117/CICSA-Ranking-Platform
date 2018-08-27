from cicsa_ranking.models import Member
from ..base.GeneralModelAPI import GeneralModelAPI


class MemberAPI(GeneralModelAPI):
    def setBaseClass(self):
        return Member
