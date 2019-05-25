import hashlib
import random
import string
from cicsa_ranking.models import Account, School
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices, DBMap
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class AccountView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = Account
        self.assoc_class_school = School
        self.validation_table = {
            'base_table_invalid': {'_state', 'account_salt', 'account_password'},
            'base_form_invalid': {'_state', 'id', 'account_salt'},
        }
        super().__init__(request, self.base_class, self.validation_table)

# View Process Functions
    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST)
            dispatcher = super().populateDispatcher()

            if dispatcher.get(action):
                account_id = kwargs.pop('id', None)
                account = self.useAPI(self.base_class).verifySelf(id=account_id)
                pwd = RequestFunctions.getSinglePostObj(post_dict, 'account_password')
                pwd_salt = account.account_salt
                if not (pwd == account.account_password):
                    hashpwd = hashlib.sha224((pwd + pwd_salt).encode("utf-8")).hexdigest()
                    account.account_password = hashpwd
            else:
                account = self.base_class()
                pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
                hashpwd = hashlib.sha224(
                    (RequestFunctions.getSinglePostObj(post_dict, 'account_password') + pwd_salt).encode("utf-8")
                ).hexdigest()
                account.account_salt = pwd_salt
                account.account_password = hashpwd

            account.account_type = RequestFunctions.getSinglePostObj(post_dict, 'account_type')
            account.account_email = RequestFunctions.getSinglePostObj(post_dict, 'account_email')
            account.account_status = RequestFunctions.getSinglePostObj(post_dict, 'account_status')
            account.account_linked_id = RequestFunctions.getSinglePostObj(post_dict, 'account_linked_id')

            if not action == 'delete':
                account.save()

            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=account.id
                )
            )

            if action == 'delete':
                account.delete()
        except Exception as e:
            print({"Error": "Cannot Process " + action.title() + " Request. " + str(e)})

# View Generating Functions
    # Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action')
        element_id = kwargs.pop('element_id')
        field_data_dispatcher = self.populateDispatcher()
        if field_data_dispatcher.get(action):
            field_data = MiscFunctions.filterDict(
                self.useAPI(self.base_class).verifySelf(
                    id=element_id
                ).__dict__.items(),
                self.validation_table['base_form_invalid']
            )
            return field_data
        return None

    def getChoiceData(self):
        choice_data = dict()
        choice_data["account_status"] = Choices().getStatusChoices()
        choice_data["account_type"] = Choices().getAccountTypeChocies()
        return choice_data

    def getDBMap(self, data):
        db_map = dict()
        db_map['account_linked_id'] = (
            lambda x: 'Unlinked' if x == -1 else
            DBMap().getMap(
                self.assoc_class_school, data['account_linked_id'], 'school_name'
            )
        )(data['account_linked_id'])
        return db_map

    def getMultiChoiceData(self):
        return None

    def getSearchElement(self, **kwargs):
        return None

    # Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if field.name not in self.validation_table['base_table_invalid']]

    def getTableRowContent(self, content):
        field_data = MiscFunctions.filterDict(
            self.useAPI(self.base_class).getSelf(id=content.id).__dict__.items(),
            self.validation_table['base_table_invalid']
        )
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData())
        field_data = self.updateDBMapAsValue(field_data, self.getDBMap(field_data))
        field_data = MiscFunctions.grabValueAsList(field_data)
        return field_data
