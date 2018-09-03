from cicsa_ranking.models import Account
from ..base.GeneralModelAPI import GeneralModelAPI


class AccountAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Account
