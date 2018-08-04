from .AbstractMutableCustomClass import *
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class EventTeamView(AbstractMutableCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = EventTeam;
        self.assoc_class_event_activity = EventActivity;
        self.assoc_class_event = Event;
        self.assoc_class_school = School;
        self.assoc_class_team = Team;
        self.assoc_class_member = MemberGroup;
        self.assoc_class_member_group = MemberGroup;
        self.form_class = EventTeamForm;
        self.search_name = ['event_team_event_member_group'];
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_team_member_group_id'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                event_team_id = kwargs.pop('id', None);
                event_team = self.base_class.objects.get(id=event_team_id);
            else:
                event_team = self.base_class();

            event_team.event_team_id = getSinglePostObj(post_dict, 'event_team_id');
            event_team.event_team_event_activity_id = getSinglePostObj(post_dict, 'event_team_event_activity_id');
            event_team.event_team_member_group_id = [getSinglePostObj(post_dict, name + "_result")
                                                     for name in self.search_name][0]

            if not action == 'delete':
                event_team.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=event_team.id));

            if action == 'delete':
                event_team.delete();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request."});

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
        return None

    def getDBMap(self, data):
        db_map = dict();
        event_activity = getModelObject(self.assoc_class_event_activity, id=data['event_team_event_activity_id']);
        event_parent = getModelObject(self.assoc_class_event, id=event_activity.event_activity_event_parent);
        db_map['event_team_event_activity_id'] = event_parent.event_name + ' - ' + event_activity.event_activity_name;
        db_map['event_team_id'] = DBMap().getMap(self.assoc_class_team, data['event_team_id'], 'team_name');
        db_map['event_team_member_group_id'] = (
            lambda x: 'Unlinked' if x is None else
            (getModelObject(self.assoc_class_member_group, id=data['event_team_member_group_id'])).member_group_name
        )(data['event_team_member_group_id']);
        return db_map;

    def getMultiChoiceData(self):
        return None;

    def getSearchElement(self, **kwargs):
        def getSearchDefault(id):
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None;
            if element_id:
                event_team = getModelObject(self.base_class, id=element_id);
                if event_team.event_team_member_group_id is not None:
                    member_group = getModelObject(self.assoc_class_member_group, id=event_team.event_team_member_group_id);
                    return member_group.id, member_group.member_group_name;
            return None, None;
        return [
                    SearchElement(self.search_name[i], 'Event Team Event Member Group', 'MemberGroup', None,
                                  'member_group_name', None, getSearchDefault(i)) for i in range(len(self.search_name))
                ];

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateDBMapAsValue(field_data, self.getDBMap(field_data));
        field_data = grabValueAsList(field_data);
        return field_data;
