import hashlib, random, string
from abc import ABC, abstractmethod

from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class EventCreationView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.form_path = '';
        self.base_class = Event;
        self.form_class = EventCreationForm;
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_team_number', 'event_rotation_detail', 'event_create_time'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions
    @abstractmethod
    def abstractFormProcess(self, action, **kwargs):
        pass;

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
        return {'event_creation_event_type': self.form_path};

    def getChoiceData(self):
        choice_data = {};
        choice_data['event_creation_event_type'] = Choices().getEventTypeChoices();
        choice_data['event_creation_event_host'] = Choices().getSchoolChoices();
        choice_data['event_creation_event_region'] = Choices().getRegionChoices();
        return choice_data;

    def getMultiChoiceData(self):
        multi_choice_data = {};
        multi_choice_data['event_creation_event_team'] = Choices().getSchoolChoices();
        return multi_choice_data;

    def getSearchElement(self, **kwargs):
        return None;

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        base_header = [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];
        additional_header = [];
        return base_header + additional_header;

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id, event_type=self.form_path).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = grabValueAsList(field_data);
        return field_data;
