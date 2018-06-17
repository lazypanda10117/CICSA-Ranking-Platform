from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class MemberView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = Member;
        self.form_class = MemberForm;
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                member_id = kwargs.pop('id', None);
                member = self.base_class.objects.get(id=member_id);
            else:
                member = self.base_class();

            member.member_name = getPostObj(post_dict, 'member_name');
            member.member_school = getPostObj(post_dict, 'member_school');
            member.member_email = getPostObj(post_dict, 'member_email');
            member.member_status = getPostObj(post_dict, 'member_status');

            if not action == 'delete':
                member.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=member.id));

            if action == 'delete':
                member.delete();
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
        choice_data["member_status"] = Choices().getStatusChoices();
        choice_data["member_school"] = Choices().getSchoolChoices();
        return choice_data;

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
