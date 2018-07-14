import hashlib, random, string

from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class AccountView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = Account;
        self.form_class = AccountForm;
        self.validation_table = {
            'base_table_invalid': {'_state', 'account_salt'},
            'base_form_invalid': {'_state', 'id', 'account_salt'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                account_id = kwargs.pop('id', None);
                account = self.base_class.objects.get(id=account_id);
                pwd = getSinglePostObj(post_dict, 'account_password');
                pwd_salt = account.account_salt;
                if not (pwd == account.account_password):
                    hashpwd = hashlib.sha224((pwd + pwd_salt).encode("utf-8")).hexdigest();
                    account.account_password = hashpwd;
            else:
                account = self.base_class();
                pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15));
                hashpwd = hashlib.sha224(
                    (getSinglePostObj(post_dict, 'account_password') + pwd_salt).encode("utf-8")).hexdigest();
                account.account_salt = pwd_salt;
                account.account_password = hashpwd;

            account.account_type = getSinglePostObj(post_dict, 'account_type');
            account.account_email = getSinglePostObj(post_dict, 'account_email');
            account.account_status = getSinglePostObj(post_dict, 'account_status');
            account.account_linked_id = getSinglePostObj(post_dict, 'account_linked_id');

            if not action == 'delete':
                account.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=account.id));

            if action == 'delete':
                account.delete();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request." });

### View Generating Functions

    ### Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action');
        element_id = kwargs.pop('element_id');
        field_data_dispatcher = self.populateDispatcher();
        if field_data_dispatcher.get(action):
            field_data = filterDict(getModelObject(self.base_class,id=element_id).__dict__.items(),
                                    self.validation_table['base_form_invalid']);
            return field_data;
        return None;

    def getChoiceData(self):
        choice_data = {};
        choice_data["account_status"] = Choices().getStatusChoices();
        choice_data["account_type"] = Choices().getAccountTypeChocies();
        return choice_data;

    def getMultiChoiceData(self):
        return {};

    def getSearchElement(self, **kwargs):
        return None;

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = grabValueAsList(field_data);
        return field_data;
