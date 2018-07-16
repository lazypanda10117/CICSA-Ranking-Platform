from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class SummaryView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = Summary;
        self.assoc_class_event = Event;
        self.form_class = SummaryForm;
        self.search_name = ['event_parent_name'];
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'summary_event_parent'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                summary_id = kwargs.pop('id', None);
                summary = self.base_class.objects.get(id=summary_id);
            else:
                summary = self.base_class();

            summary.summary_event_parent = [getSinglePostObj(post_dict, name + "_result") for name in self.search_name][0];
            summary.summary_event_school = getSinglePostObj(post_dict, 'summary_event_school');
            summary.summary_event_ranking = getSinglePostObj(post_dict, 'summary_event_ranking');
            summary.summary_event_override_ranking = getSinglePostObj(post_dict, 'summary_event_override_ranking');
            summary.summary_event_score = getSinglePostObj(post_dict, 'summary_event_score');

            if not action == 'delete':
                summary.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=summary.id));

            if action == 'delete':
                summary.delete();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request." });

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
        return None;

    def getChoiceData(self):
        choice_data = dict();
        choice_data['summary_event_school'] = Choices().getSchoolChoices();
        return choice_data;

    def getDBMap(self, data):
        db_map = dict();
        db_map['summary_event_parent'] = DBMap().getMap(self.assoc_class_event,
                                                        data['summary_event_parent'], 'event_name');
        return db_map;

    def getMultiChoiceData(self):
        return None;

    def getSearchElement(self, **kwargs):
        def getSearchDefault(id):
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None;
            if element_id:
                summary = getModelObject(self.base_class, id=element_id);
                if summary.summary_event_parent is not None:
                    event_parent = getModelObject(Event, id=summary.summary_event_parent);
                    return event_parent.id, event_parent.event_name + ' (' + event_parent.event_host + ')';
            return None, None;
        return [
                    SearchElement(self.search_name[i], 'Summary Event Parent', 'Event', '', 'event_name', 'event_host',
                                  getSearchDefault(i)) for i in range(len(self.search_name))
                ];

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = self.updateDBMapAsValue(field_data, self.getDBMap(field_data));
        field_data = grabValueAsList(field_data);
        return field_data;
