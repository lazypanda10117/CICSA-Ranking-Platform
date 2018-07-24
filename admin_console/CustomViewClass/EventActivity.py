from .AbstractMutableCustomClass import AbstractMutableCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class EventActivityView(AbstractMutableCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = EventActivity;
        self.assoc_class_event = Event;
        self.assoc_class_event_tag = EventTag;
        self.form_class = EventActivityForm;
        self.search_name = ['event_activity_event_parent', 'evnet_activity_event_tag'];
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_activity_event_parent', 'event_activity_event_tag'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                event_activity_id = kwargs.pop('id', None);
                event_activity = self.base_class.objects.get(id=event_activity_id);
            else:
                event_activity = self.base_class();

            event_activity.event_activity_event_parent = [getSinglePostObj(post_dict, self.search_name[0] + "_result")][0];
            event_activity.event_activity_event_tag = [getSinglePostObj(post_dict, self.search_name[1] + "_result")][0];
            event_activity.event_activity_name = getSinglePostObj(post_dict, 'event_activity_name');
            event_activity.event_activity_order = getSinglePostObj(post_dict, 'event_activity_order');
            event_activity.event_activity_result = getSinglePostObj(post_dict, 'event_activity_result');
            event_activity.event_activity_type = getSinglePostObj(post_dict, 'event_activity_type');
            event_activity.event_activity_note = getSinglePostObj(post_dict, 'event_activity_note');
            event_activity.event_activity_status = getSinglePostObj(post_dict, 'event_activity_status');

            if not action == 'delete':
                event_activity.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=event_activity.id));

            if action == 'delete':
                event_activity.delete();
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
        choice_data['event_activity_type'] = Choices().getEventActivityTypeChoices();
        choice_data['event_activity_status'] = Choices().getEventStatusChoices();
        return choice_data;

    def getDBMap(self, data):
        db_map = dict();
        db_map['event_activity_event_parent'] = DBMap().getMap(self.assoc_class_event,
                                                        data['event_activity_event_parent'], 'event_name');
        db_map['event_activity_event_tag'] = DBMap().getMap(self.assoc_class_event_tag,
                                                               data['event_activity_event_tag'], 'event_tag_name');
        return db_map;

    def getMultiChoiceData(self):
        return None;

    def getSearchElement(self, **kwargs):
        element_id = kwargs['element_id'] if 'element_id' in kwargs else None
        def searchDefaultAbstract0():
            if element_id:
                event_activity = getModelObject(self.base_class, id=element_id);
                if event_activity.event_activity_event_parent is not None:
                    event_parent = getModelObject(self.assoc_class_event, id=event_activity.event_activity_event_parent);
                    return event_parent;
            return None;

        def getSearchDefault0():
            return (lambda x: (None, None) if x is None else
            (x.id, x.event_name + ' (' + str(x.event_host) + ')'))(searchDefaultAbstract0());

        def getSearchDefault1():
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None;
            if element_id:
                event_activity = getModelObject(self.base_class, id=element_id);
                if event_activity.event_activity_event_parent is not None:
                    event_tag = getModelObject(self.assoc_class_event_tag, id=event_activity.event_activity_event_tag);
                    return event_tag.id, event_tag.event_tag_name + ' (' + str(event_tag.event_tag_event_id) + ')';
            return None, None;

        def getSearchKeyDict(field_name):
            return (lambda x: x if x is None else {field_name: x.id})(searchDefaultAbstract0());

        return [
                    SearchElement(self.search_name[0], 'Event Activity Event Parent (Unalterable)',
                                  'Event', getSearchKeyDict("id"), 'event_name', 'event_host', getSearchDefault0()),
                    SearchElement(self.search_name[1], 'Event Activity Event Tag',
                                  'EventTag', getSearchKeyDict("event_tag_event_id"), 'event_tag_name',
                                  'event_tag_event_id', getSearchDefault1())
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
