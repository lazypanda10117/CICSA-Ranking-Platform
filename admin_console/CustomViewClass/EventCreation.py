import hashlib, random, string

from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *
from .FleetLogic import *
from .GroupLogic import *

from ..models import *
from ..forms import *

class EventCreationView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.form_path = '';
        self.base_class = Event;
        self.form_class = EventCreationForm;
        self.search_name = ['member0', 'member1'];
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_team_number', 'event_rotation_detail', 'event_create_time'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### Class Custom Functions
    def __setLogicDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('fleet', FleetLogic);
        dispatcher.add('group', GroupLogic);
        return dispatcher;

### Function Override
    def grabData(self, *args):
        self.form_path= args[1];
        super().grabData(self, *args);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            self.form_path = getPostObj(post_dict, 'event_creation_event_type');
            logic = self.__setLogicDispatcher().get(self.form_path)(post_dict);

            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None);
                if action == 'edit':
                    logic._edit(event_creation_id);
                elif action == 'delete':
                    logic._delete(event_creation_id);
            else:
                if action == 'add':
                    logic._add();
            #loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=member_group.id));
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
        choice_data["member_group_school"] = Choices().getSchoolChoices();
        return choice_data;

    def getSearchElement(self, **kwargs):
        return None;

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        print ('hello world');
        base_header = [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];
        additional_header = [];
        return base_header + additional_header;

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = grabValueAsList(field_data);
        return field_data;
