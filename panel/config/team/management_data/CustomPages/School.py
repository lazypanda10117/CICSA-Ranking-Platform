import hashlib
import random
import string
from cicsa_ranking.models import School, Account
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class SchoolView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = School
        self.assoc_class_account = Account
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id'},
            'account_invalid': {'_state', 'id', 'account_type', 'account_salt', 'account_status', 'account_linked_id'}
        }
        super().__init__(request, self.base_class, self.validation_table)

# View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST)
            dispatcher = super().populateDispatcher()

            if dispatcher.get(action):
                school_id = kwargs.pop('id', None)
                school = self.useAPI(self.base_class).verifySelf(id=school_id)
                school_account = self.useAPI(self.assoc_class_account).verifySelf(account_linked_id=school.id)
                pwd = RequestFunctions.getSinglePostObj(post_dict, 'account_password')
                pwd_salt = school_account.account_salt
                if not (pwd == school_account.account_password):
                    hashpwd = hashlib.sha224((pwd + pwd_salt).encode("utf-8")).hexdigest()
                    school_account.account_password = hashpwd
            else:
                school = self.base_class()
                school_account = self.assoc_class_account()
                pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
                hashpwd = hashlib.sha224(
                    (
                            RequestFunctions.getSinglePostObj(
                                post_dict, 'account_password'
                            ) + pwd_salt
                    ).encode("utf-8")).hexdigest()
                school_account.account_type = "school"
                school_account.account_salt = pwd_salt
                school_account.account_password = hashpwd

            school.school_name = RequestFunctions.getSinglePostObj(post_dict, 'school_name')
            school.school_region = RequestFunctions.getSinglePostObj(post_dict, 'school_region')
            school.school_status = RequestFunctions.getSinglePostObj(post_dict, 'school_status')
            school.school_season_score = RequestFunctions.getSinglePostObj(post_dict, 'school_season_score')
            school.school_default_team_name = RequestFunctions.getSinglePostObj(post_dict, 'school_default_team_name')
            if not action == 'delete':
                school.save()

            LogFunctions.loghelper(
                self.request, 'admin', LogFunctions.logQueryMaker(
                    self.base_class, action.title(), id=school.id))
            school_account.account_email = RequestFunctions.getSinglePostObj(post_dict, 'account_email')
            school_account.account_status = RequestFunctions.getSinglePostObj(post_dict, 'school_status')
            school_account.account_linked_id = school.id
            if not action == 'delete':
                school_account.save()

            LogFunctions.loghelper(
                self.request, 'admin', LogFunctions.logQueryMaker(
                    Account, action.title(), id=school_account.id))

            if action == 'delete':
                school.delete()
                school_account.delete()
        except Exception:
            print({"Error": "Cannot Process " + action.title() + " Request."})

# View Generating Functions

    # Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action')
        element_id = kwargs.pop('element_id')
        field_data_dispatcher = self.populateDispatcher()
        if field_data_dispatcher.get(action):
            base_data = MiscFunctions.filterDict(
                self.useAPI(self.base_class).getSelf(id=element_id).__dict__.items(),
                self.validation_table['base_form_invalid']
            )
            account_data = MiscFunctions.filterDict(
                self.useAPI(self.assoc_class_account).getSelf(account_linked_id=element_id).__dict__.items(),
                self.validation_table['account_invalid']
            )
            field_data = {**base_data, **account_data}
            return field_data
        return None

    def getChoiceData(self):
        choice_data = dict()
        choice_data["school_region"] = Choices().getRegionChoices()
        choice_data["school_status"] = Choices().getStatusChoices()
        return choice_data

    def getDBMap(self, data):
        return None

    def getMultiChoiceData(self):
        return None

    def getSearchElement(self, **kwargs):
        return None

    # Table Generating Functions
    def getTableSpecificHeader(self):
        return [
                   field.name for field in self.base_class._meta.get_fields()
                   if field.name not in self.validation_table['base_table_invalid']
               ] + ["account_email", "account_password"]

    def getTableRowContent(self, content):
        base_data = MiscFunctions.filterDict(self.useAPI(self.base_class).getSelf(id=content.id).
                                             __dict__.items(), self.validation_table['base_table_invalid'])
        base_data = self.updateChoiceAsValue(base_data, self.getChoiceData())
        base_data = MiscFunctions.grabValueAsList(base_data)
        try:
            account_data = MiscFunctions.grabValueAsList(
                MiscFunctions.filterDict(
                    self.useAPI(self.assoc_class_account).getSelf(account_linked_id=content.id).
                    __dict__.items(), self.validation_table['account_invalid']))
        except Exception:
            account_data = MiscFunctions.grabValueAsList({'account_email': '', 'account_password': ''})

        field_data = base_data + account_data
        return field_data
