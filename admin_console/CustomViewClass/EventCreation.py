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
        self.form_path = self.setFormPath();
        self.base_class = Event;
        self.form_class = EventCreationForm;
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_team_number', 'event_rotation_detail', 'event_create_time'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### Class Specific Function
    @abstractmethod
    def setFormPath(self):
        pass;

### Overriding Function
    def setViewDispatcher(self):
        dispatcher = super().setViewDispatcher();
        dispatcher.update('edit', False);
        dispatcher.update('delete', False);
        return dispatcher;

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
            field_data = filterDict(getModelObject(self.base_class, id=element_id).__dict__.items(),
                                    self.validation_table['base_form_invalid']);
            return field_data;
        return {'event_type': self.form_path};

    def getChoiceData(self):
        choice_data = {};
        choice_data['event_type'] = Choices().getEventTypeChoices();
        choice_data['event_status'] = Choices().getEventStatusChoices();
        choice_data['event_host'] = Choices().getSchoolChoices();
        choice_data['event_region'] = Choices().getRegionChoices();
        return choice_data;

    def getDBMap(self, data):
        return None;

    def getMultiChoiceData(self):
        multi_choice_data = {};
        multi_choice_data['event_team'] = Choices().getSchoolChoices();
        return multi_choice_data;

    def getSearchElement(self, **kwargs):
        return None;

    def getTableRow(self, content):
        rowContent = {};
        rowContent["db_content"] = self.getTableRowContent(content);
        return rowContent;

    ### Table Generating Functions
    def getTableHeader(self):
        return self.getTableSpecificHeader();

    def getTableSpecificHeader(self):
        base_header = [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];
        additional_header = [];
        return base_header + additional_header;

    def getTableRowContent(self, content):
        event_types = {type_name: type_id for type_id, type_name in Choices().getEventTypeChoices()}
        field_data = filterDict(getModelObject(
            self.base_class, id=content.id, event_type=event_types[self.form_path]).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = grabValueAsList(field_data);
        return field_data;