import json, random
from abc import ABC, abstractmethod

from .AbstractMutableCustomClass import AbstractMutableCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *


class EventCreationView(AbstractMutableCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = Event;
        self.form_class = EventCreationForm;
        self.validation_table = {
            'base_table_invalid': {'_state', 'event_schools'},
            'base_form_invalid': {'_state', 'id', 'event_team_number', 'event_schools', 'event_school_ids',
                                  'event_rotation_detail', 'event_create_time'},
        };
        super().__init__(request, self.base_class, self.validation_table);
        self.form_path = self.setFormPath();
        self.event_types = {type_name: type_id for type_id, type_name in Choices().getEventTypeChoices()};


### Class Specific Function
    @abstractmethod
    def setFormPath(self):
        pass;

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
            field_data = self.serializeJSONListData(['event_school_ids', 'event_rotation_detail'], field_data);
            return field_data;
        return {'event_type': self.form_path};


    def getChoiceData(self):
        choice_data = {};
        choice_data['event_type'] = Choices().getEventTypeChoices();
        choice_data['event_status'] = Choices().getEventStatusChoices();
        choice_data['event_host'] = Choices().getSchoolChoices();
        choice_data['event_season'] = Choices().getSeasonChoices();
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

    ### Table Generating Functions
    def getTableContent(self, **kwargs):
        arg_dict = {} if self.form_path == 'all' else {"event_type": self.event_types[self.form_path]};
        return super().getTableContent(**{**arg_dict, **kwargs});

    def getTableHeader(self):
        return self.getTableSpecificHeader();

    def getTableSpecificHeader(self):
        base_header = [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];
        additional_header = [];
        return base_header + additional_header;

    def getTableRow(self, content):
        rowContent = {};
        rowContent["db_content"] = self.getTableRowContent(content);
        return rowContent;

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = self.serializeJSONListData(['event_school_ids', 'event_rotation_detail'], field_data);
        field_data = grabValueAsList(field_data);
        return field_data;