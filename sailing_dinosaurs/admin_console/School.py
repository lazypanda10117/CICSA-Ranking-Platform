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
        super().__init__(request, self.base_class);

### View Process Functions

    def add(self):
        try:
            school_name= self.request.POST.get("name");
            school_email = self.request.POST.get("email");
            school_pwd = self.request.POST.get("password");
            school_region = self.request.POST.get("region"); #integer
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
            return HttpResponse('{"Response": "Error: Cannot Create School."}');

    def edit(self, id):
        pass;

    def delete(self, id):
        pass;

### View Generating Functions

    def grabData(self, *args):
        return super().grabData(*args);

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

        if field_data_dispatcher.get(action):
            base_data = self.base_class.objects.get(id=element_id).__dict__;
            account_data = Account.objects.get(account_linked_id=element_id).__dict__;
            field_data = {key: account_data[key] for key in account_data.keys() & {'account_email', 'account_password'}}
            return {**base_data, **field_data};

        return None;

    def getChoiceData(self):
        choice_data = {};
        choice_data["region"] = Choices.REGION_CHOICES;
        choice_data["status"] = Choices.STATUS_CHOICES;
        return choice_data;

    def grabFormData(self, **kwargs):
        return super().grabFormData(**kwargs);

    ### Table Generating Functions
    def getTableHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()] + \
               ["account_email", "account_password", "edit", "delete"];

    def getTableRow(self, content):
        rowContent = {};
        rowContent["db_content"] = '';
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id));
        pass;

    def makeEditDeleteBtn(self, path, id):
        editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
        deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn];

    def getTableContent(self):
        return super().getTableContent();

    def grabTableData(self, form_path):
        return super().grabTableData(form_path);
