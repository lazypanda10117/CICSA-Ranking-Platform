from cicsa_ranking.models import Account
from api.base.GeneralModelAPI import GeneralModelAPI
from api.model_api.SchoolAPI import SchoolAPI


class AccountAPI(GeneralModelAPI):
    @staticmethod
    def getBaseClass():
        return Account

    def getAssociatedNameById(self, account_id):
        account = self.getSelf(id=account_id)
        if account.account_type == Account.ACCOUNT_ADMIN:
            return "Admin"
        elif account.account_type == Account.ACCOUNT_SCHOOL:
            associated_school = SchoolAPI(self.request).getSelf(id=account.account_linked_id)
            return associated_school.school_name
        else:
            return "Anonymous"

    def getAdminIDs(self):
        return [account.id for account in AccountAPI(self.request).filterSelf(account_type="admin")]
