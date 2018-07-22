import json
from ..HelperClass import *
from ..generalFunctions import *
from .EventCreation import *

from ..models import *

class EventView(EventCreationView):
    def __init__(self, request):
        super().__init__(request);
        self.form_class = EventForm;
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_team_number', 'event_create_time'},
        };

        self.assoc_class_activity = EventActivity;
        self.assoc_class_team = Team;
        self.assoc_class_school = School;
        self.assoc_class_team_link = EventTeam;
        self.assoc_class_tag = EventTag;
        self.assoc_class_summary = Summary;
        self.assoc_class_season = Season;


        self.event_race_tag = ["Fleet A", "Fleet B"];
        self.event_team_name_suffix = ["Team A", "Team B"];
        self.event_activity_type = "race";

    def setFormPath(self):
        return 'all';

    def setViewDispatcher(self):
        return AbstractCustomClass.setViewDispatcher(self);

    def getTableHeader(self):
        return self.getTableSpecificHeader() + ["edit", "delete"];

    def getTableRow(self, content):
        rowContent = dict();
        rowContent["db_content"] = self.getTableRowContent(content);
        rowContent["button"] = self.makeEditDeleteBtn('custom', str(content.id));
        return rowContent;

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);

            event_type = getSinglePostObj(post_dict, 'event_type');
            event_name = getSinglePostObj(post_dict, 'event_name');
            event_status = getSinglePostObj(post_dict, 'event_status');
            event_description = getSinglePostObj(post_dict, 'event_description');
            event_location = getSinglePostObj(post_dict, 'event_location');
            event_season = getSinglePostObj(post_dict, 'event_season');
            event_region = getSinglePostObj(post_dict, 'event_region');
            event_host = getSinglePostObj(post_dict, 'event_host');
            event_school = getMultiplePostObj(post_dict, 'event_team');
            event_race_number = getSinglePostObj(post_dict, 'event_race_number');
            event_boat_rotation_name = getSinglePostObj(post_dict, 'event_boat_rotation_name');
            event_rotation_detail = getSinglePostObj(post_dict, 'event_rotation_detail');
            event_start_date = getSinglePostObj(post_dict, 'event_start_date');
            event_end_date = getSinglePostObj(post_dict, 'event_end_date');

            event_season_name = getModelObject(self.assoc_class_season, id=event_season).season_name;
            try:
                event_json_rotation_detail = json.loads(event_rotation_detail);
            except:
                event_json_rotation_detail = {};

            dispatcher = super().populateDispatcher();
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None);
                event_creation = self.base_class.objects.get(id=event_creation_id);
            else:
                event_creation = self.base_class();

            # event generation
            event_creation.event_type = int(event_type);
            event_creation.event_name = event_name + ' - ' + event_season_name;
            event_creation.event_status = event_status;
            event_creation.event_description = event_description;
            event_creation.event_location = event_location;
            event_creation.event_season = int(event_season);
            event_creation.event_region = int(event_region);
            event_creation.event_host = int(event_host);
            event_creation.event_race_number = int(event_race_number);
            event_creation.event_boat_rotation_name = event_boat_rotation_name;
            event_creation.event_start_date = event_start_date;
            event_creation.event_end_date = event_end_date;
            event_creation.event_team_number = 0 if event_school is None else len(event_school);
            event_creation.event_rotation_detail = event_json_rotation_detail;
            event_creation.save();
            loghelper(self.request, 'admin',
                      logQueryMaker(self.base_class, action.title(), id=event_creation.id))
        except Exception as e:
            print({"Error": "Cannot Process " + action.title() + " Request." });
            print(e);