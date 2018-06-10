from django.db import transaction
import hashlib, random, string

from .Dispatcher import Dispatcher
from .AbstractCustomClass import AbstractCustomClass
from .generalFunctions import *
from .CustomElement import *

from .models import *
from .forms import *

class SchoolView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = School;
        self.form_class = SchoolForm;
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id'},
            'account_invalid': {'_state', 'id', 'account_type', 'account_salt', 'account_status', 'account_linked_id'}
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions
    def genericProcess(self, action):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();
            if dispatcher.get(action):
                school = School.objects.get(id=id);
                school_account = Account.objects.get(account_linked_id=school.id);
                pwd = getPostObj(post_dict, 'account_password');
                pwd_salt = school_account.account_salt;
                if not (pwd == school_account.account_password):
                    hashpwd = hashlib.sha224((pwd + pwd_salt).encode("utf-8")).hexdigest();
                    school_account.account_password = hashpwd;
            else:
                school = School();
                school_account = Account();
                pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15));
                hashpwd = hashlib.sha224(
                    (getPostObj(post_dict, 'account_password') + pwd_salt).encode("utf-8")).hexdigest();
                school_account.account_password = hashpwd;

            school.school_name = getPostObj(post_dict, 'school_name');
            school.school_region = getPostObj(post_dict, 'school_region');
            school.school_status = getPostObj(post_dict, 'school_status');
            school.school_season_score = getPostObj(post_dict, 'school_season_score');
            school.save();
            loghelper(self.request, 'admin', logQueryMaker(School, 'Edit', id=school.id));
            school_account.account_email = getPostObj(post_dict, 'account_email');
            school_account.account_status = getPostObj(post_dict, 'school_status');
            school_account.account_linked_id = school.id;
            school_account.save();
            loghelper(self.request, 'admin', logQueryMaker(Account, action.title(), id=school_account.id));
        except:
            return {"Error": "Cannot Process " + action.title() + " Request." };

    def add(self):
        try:
            post_dict = dict(self.request.POST);
            pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15));
            hashpwd = hashlib.sha224((getPostObj(post_dict, 'account_password') + pwd_salt).encode("utf-8")).hexdigest();
            school = School();
            school.school_name = getPostObj(post_dict, 'school_name');
            school.school_region = getPostObj(post_dict, 'school_region');
            school.school_status = getPostObj(post_dict, 'school_status');
            school.school_season_score = getPostObj(post_dict, 'school_season_score');
            school.save();
            school_id = str(school.id);
            loghelper(self.request, 'admin',
                      "Add School id: " + school_id + " and name: " + getPostObj(post_dict, 'school_name'));
            school_account = Account();
            school_account.account_type = "school";
            school_account.account_email = getPostObj(post_dict, 'account_email');
            school_account.account_salt = pwd_salt;
            school_account.account_password = hashpwd;
            school_account.account_status = getPostObj(post_dict, 'school_status');
            school_account.account_linked_id = school_id;
            school_account.save();
            school_account_id = str(school_account.id);
            loghelper(self.request, 'admin', "Edit Account id: " +
                      school_account_id + " and type: school and email: " + getPostObj(post_dict, 'account_email'));
        except:
            return {"Error":  "Cannot Process"};

    def edit(self, id):
        try:
            post_dict = dict(self.request.POST);
            school = School.objects.get(id=id);
            school.school_name = getPostObj(post_dict, 'school_name');
            school.school_region = getPostObj(post_dict, 'school_region');
            school.school_status = getPostObj(post_dict, 'school_status');
            school.school_season_score = getPostObj(post_dict, 'school_season_score');
            school.save();
            loghelper(self.request, 'admin', logQueryMaker(School, 'Edit', id=school.id));
            school_account = Account.objects.get(account_linked_id=school.id);
            pwd = getPostObj(post_dict, 'account_password');
            pwd_salt = school_account.account_salt;
            if not (pwd == school_account.account_password):
                hashpwd = hashlib.sha224((pwd + pwd_salt).encode("utf-8")).hexdigest();
                school_account.account_password = hashpwd;
            school_account.account_email = getPostObj(post_dict, 'account_email');
            school_account.account_status = getPostObj(post_dict, 'school_status');
            school_account.save();
            loghelper(self.request, 'admin', logQueryMaker(Account, 'Edit', id=school_account.id));
        except:
            return {"Error":  "Cannot Process"};

    def delete(self, id):
        pass;

### View Generating Functions

    ### Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action');
        element_id = kwargs.pop('element_id');
        field_data_dispatcher = self.populateDispatcher();
        if field_data_dispatcher.get(action):
            base_data = filterDict(getModelObject(self.base_class,id=element_id).__dict__.items(), self.validation_table['base_form_invalid']);
            account_data = filterDict(getModelObject(Account, account_linked_id=element_id).__dict__.items(), self.validation_table['account_invalid']);
            field_data = {**base_data, **account_data};
            return field_data;
        return None;

    def getChoiceData(self):
        choice_data = {};
        choice_data["school_region"] = Choices.REGION_CHOICES;
        choice_data["school_status"] = Choices.STATUS_CHOICES;
        return choice_data;

    ### Table Generating Functions
    def getTableHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()] + \
               ["account_email", "account_password", "edit", "delete"];

    def getTableRowContent(self, content):
        base_data = grabValueAsList(filterDict(getModelObject(self.base_class, id=content.id).
                                               __dict__.items(), self.validation_table['base_table_invalid']));
        try:
            account_data = grabValueAsList(filterDict(getModelObject(Account, account_linked_id=content.id).
                                                      __dict__.items(), self.validation_table['account_invalid']));
        except:
            account_data = grabValueAsList({'account_email': '', 'account_password': ''});

        field_data = base_data + account_data;
        return field_data;
