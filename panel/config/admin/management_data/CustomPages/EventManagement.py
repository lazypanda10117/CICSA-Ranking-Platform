from abc import abstractmethod

from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices
from misc.CustomFunctions import MiscFunctions
from cicsa_ranking.models import Event


class EventManagementView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = Event
        self.validation_table = {
            'base_table_invalid': {'_state', 'event_rotation_detail'},
            'base_form_invalid': {'_state', 'id', 'event_team_number', 'event_school_ids',
                                  'event_rotation_detail', 'event_create_time'},
        }
        super().__init__(request, self.base_class, self.validation_table)
        self.form_path = self.setFormPath()
        self.event_types = {type_name: type_id for type_id, type_name in Choices().getEventTypeChoices()}


# Class Specific Function
    @abstractmethod
    def setFormPath(self):
        pass

# View Process Functions
    @abstractmethod
    def abstractFormProcess(self, action, **kwargs):
        pass

# View Generating Functions

    # Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action')
        element_id = kwargs.pop('element_id')
        field_data_dispatcher = self.populateDispatcher()
        if field_data_dispatcher.get(action):
            raw_data = self.useAPI(self.base_class).verifySelf(id=element_id).__dict__
            field_data = MiscFunctions.filterDict(raw_data.items(), self.validation_table['base_form_invalid'])
            field_data['event_team'] = raw_data['event_school_ids']
            field_data = self.serializeJSONListData(['event_school_ids', 'event_rotation_detail'], field_data)
            return field_data
        return {'event_type': self.form_path}

    def getChoiceData(self):
        choice_data = dict()
        choice_data['event_type'] = Choices().getEventTypeChoices()
        choice_data['event_status'] = Choices().getEventStatusChoices()
        choice_data['event_host'] = Choices().getSchoolChoices()
        choice_data['event_season'] = Choices().getSeasonChoices()
        choice_data['event_region'] = Choices().getRegionChoices()
        return choice_data

    def getDBMap(self, data):
        return None

    def getMultiChoiceData(self):
        multi_choice_data = dict()
        multi_choice_data['event_team'] = Choices().getSchoolChoices()
        return multi_choice_data

    def getSearchElement(self, **kwargs):
        return None

    # Table Generating Functions
    def getTableContent(self, **kwargs):
        arg_dict = {} if self.form_path == 'all' else {"event_type": self.event_types[self.form_path]}
        return super().getTableContent(**{**arg_dict, **kwargs})

    def getTableSpecificHeader(self):
        base_header = [field.name for field in self.base_class._meta.get_fields()
                       if field.name not in self.validation_table['base_table_invalid']]
        additional_header = []
        return base_header + additional_header

    def getTableRowContent(self, content):
        field_data = MiscFunctions.filterDict(
            self.useAPI(self.base_class).getSelf(id=content.id).__dict__.items(),
            self.validation_table['base_table_invalid']
        )
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData())
        field_data = self.serializeJSONListData(['event_school_ids', 'event_rotation_detail'], field_data)
        field_data = MiscFunctions.grabValueAsList(field_data)
        return field_data
