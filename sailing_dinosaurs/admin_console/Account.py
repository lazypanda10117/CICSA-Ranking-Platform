from django.db import transaction
import hashlib, random, string

from .AbstractCustomClass import AbstractCustomClass
from .Dispatcher import Dispatcher
from .CustomElement import *
from .generalFunctions import *

from .models import *
from .forms import *

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
                pwd = getPostObj(post_dict, 'account_password');
                pwd_salt = account.account_salt;
                if not (pwd == account.account_password):
                    hashpwd = hashlib.sha224((pwd + pwd_salt).encode("utf-8")).hexdigest();
                    account.account_password = hashpwd;
            else:
                account = self.base_class();
                pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15));
                hashpwd = hashlib.sha224(
                    (getPostObj(post_dict, 'account_password') + pwd_salt).encode("utf-8")).hexdigest();
                account.account_salt = pwd_salt;
                account.account_password = hashpwd;

            account.account_type = getPostObj(post_dict, 'account_type');
            account.account_email = getPostObj(post_dict, 'account_email');
            account.account_status = getPostObj(post_dict, 'account_status');
            account.account_linked_id = getPostObj(post_dict, 'account_linked_id');

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
        choice_data["account_status"] = Choices.STATUS_CHOICES;
        choice_data["account_type"] = Choices.ACCOUNT_TYPE_CHOICES;
        return choice_data;

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];

    def getTableRowContent(self, content):
        field_data = grabValueAsList(filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']));
        return field_data;
