import hashlib, random, string

from .AbstractCustomClass import AbstractCustomClass
from .generalFunctions import *
from .CustomElement import *

from .models import *
from .forms import *

class SchoolView(AbstractCustomClass):

    ###
    ### Constructor <-> AbstractCustomClass
    ###

    def __init__(self, request):
        self.base_class = School;
        super().__init__(request, self.base_class);


    ###
    ### View Process Functions
    ###

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


    ###
    ### View Generating Functions
    ###

    def grabFormData(self, action):
        pass;

    def getTableHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()] + \
               ["account_email", "account_password", "edit", "delete"];

    def makeEditDeleteBtn(self, path, id):
        editBtn = Button('Edit', 'info', generateGETURL(path, {"action": 'edit', "element_id": id}));
        deleteBtn = Button('Delete', 'danger', generateGETURL(path, {"action": 'delete', "element_id": id}))
        return [editBtn, deleteBtn];

    def getTableRow(self, content):
        rowContent = {};
        rowContent["db_content"] = '';
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id));
        pass;


    ###
    ### Full Reusable Functions
    ###

    def getTableContent(self):
        return super().getTableContent();

    def grabTableData(self, form_path):
        return super().grabTableData(form_path);

    def grabData(self, action, form_path):
        return super().grabData(action, form_path);