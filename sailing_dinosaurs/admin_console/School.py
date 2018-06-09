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
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id'},
            'account_invalid': {'_state', 'id', 'account_type', 'account_salt', 'account_status', 'account_linked_id'}
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def add(self):
        try:
            print("hello");
            school_name= self.request.POST.get("school_name");
            school_email = self.request.POST.get("school_email");
            school_pwd = self.request.POST.get("school_password");
            school_region = self.request.POST.get("school_region");
            pwd_salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15));
            hashpwd = hashlib.sha224((school_pwd + pwd_salt).encode("utf-8")).hexdigest();
            school = School(school_name=school_name, school_region=school_region, school_status="active", school_season_score=0);
            school.save();
            school_id = school.id;
            loghelper(self.request, "Add School id: " + school_id + " and name: " + school_name);
            school_account = Account(account_type="school", account_email=school_email, account_salt=pwd_salt, account_pwd=hashpwd, account_status="active", account_link_id=school_id);
            school_account.save();
            loghelper(self.request, "Add Account id: " + school_account.id + " and type: school and email: " + school_email);
        except:
            return {"Error":  "Cannot Create School"};

    def edit(self, id):
        pass;

    def delete(self, id):
        pass;

### View Generating Functions

    ### Form Generating Functions
    def getFieldData(self, **kwargs):
        def populateDispatcher():
            dispatcher = Dispatcher();
            dispatcher.add('add', False);
            dispatcher.add('edit', True);
            dispatcher.add('delete', True);
            return dispatcher;

        action = kwargs.pop('action');
        element_id = kwargs.pop('element_id');
        field_data_dispatcher = populateDispatcher();

        #TODO: school_season_score default 0 for user
        #TODO: auth wrapper of whole app
        #TODO: does not exist catcher wrapper funciton

        if field_data_dispatcher.get(action):
            base_data = filterDict(self.base_class.objects.get(id=element_id).__dict__.items(), self.validation_table['base_form_invalid']);
            account_data = filterDict(Account.objects.get(account_linked_id=element_id).__dict__.items(), self.validation_table['account_invalid']);
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
        base_data = grabValueAsList(filterDict(self.base_class.objects.get(id=content.id).__dict__.items(),
                                   self.validation_table['base_table_invalid']));
        try:
            account_data = grabValueAsList(filterDict(Account.objects.get(account_linked_id=content.id).__dict__.items(),
                                      self.validation_table['account_invalid']));
        except:
            account_data = grabValueAsList({'account_email': '', 'account_password': ''});

        field_data = base_data + account_data;
        return field_data;

    def makeEditDeleteBtn(self, path, id):
        editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
        deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn];