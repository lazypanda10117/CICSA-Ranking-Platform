from ..HelperClass import *
from ..generalFunctions import *
from .EventCreationView import *

from ..models import *


class FleetCreationView(EventCreationView):
    def __init__(self, request):
        self.assoc_class_activity = EventActivity;
        self.assoc_class_team = Team;
        self.assoc_class_school = School;
        self.assoc_class_team_link = EventTeam;
        self.assoc_class_tag = EventTag;
        self.assoc_class_summary = Summary;

        self.event_race_tag = ["Fleet A", "Fleet B"];
        self.event_team_name_suffix = ["Team A", "Team B"];
        self.event_activity_base_name = 'Fleet Race ';
        self.event_activity_type = "race";
        super().__init__(request);

    def abstractFormProcess(self, action, **kwargs):
        def add():
            race_tag_dict = dict();
            team_activity_dict = dict();
            #event generation
            event_creation = self.base_class();
            event_creation.event_type = event_type;
            event_creation.event_name = event_name;
            event_creation.event_status = event_status;
            event_creation.event_description = event_description;
            event_creation.event_location = event_location;
            event_creation.event_region = event_region;
            event_creation.event_host = event_host;
            event_creation.event_boat_number = event_num_boat;
            event_creation.event_race_number = event_num_race;
            event_creation.event_start_date = event_start_date;
            event_creation.event_end_date = event_end_date;
            event_creation.event_create_time = getTimeNow();
            event_creation.event_team_number = len(event_school);
            event_creation.event_rotation_detail = self.rotationGenerator(
                event_creation.event_team_number, event_creation.event_boat_number, event_creation.event_race_number);
            event_creation.save();

            for school_id in event_school:
                school = self.assoc_class_school().objects.get(id=school_id);
                #summary generation
                self.assoc_class_summary.summary_event_parent = event_creation.id;
                self.assoc_class_summary.summary_event_school = school_id;
                self.assoc_class_summary.save();
                #team generation
                for index, suffix in enumerate(self.event_team_name_suffix):
                    team = self.assoc_class_team();
                    team_name = school.school_default_team_name + ' ' + suffix;
                    team.team_name = team_name;
                    team.team_school = school;
                    team.team_status = "active";
                    team.save();
                    team_activity_dict[race_tag_dict[index]].append(team.id);

            #event tag generation
            for tag in self.event_race_tag:
                event_tag = self.assoc_class_tag();
                event_tag.event_tag_event_id = event_creation.id;
                event_tag.event_tag_name = tag;
                event_tag.save();
                race_tag_dict[tag] = event_tag.id;

            for tag, tag_id in race_tag_dict.items():
                for i in range(event_num_race):
                    #event activity generation
                    event_activity = self.assoc_class_activity();
                    event_activity.event_activity_event_parent = event_creation.id;
                    event_activity.event_activity_event_tag = tag_id;
                    event_activity.event_activity_name = self.event_activity_base_name + str(i+1);
                    event_activity.event_activity_order = i+1;
                    event_activity.event_activity_result = dict();
                    event_activity.event_activity_note = "";
                    event_activity.event_activity_type = self.event_activity_type;
                    event_activity.event_activity_status = "future";
                    event_activity.save();
                    #event team link generation
                    event_team = self.assoc_class_team_link();
                    event_team.event_team_event_activity_id = event_activity.id;
                    event_team.event_team_id = team_activity_dict[tag][i]
                    event_team.save();

        def edit(key):
            event_creation = self.base_class.objects.get(id=key);
            pass;

        def delete(key):
            event_creation = self.base_class.objects.get(id=key);
            pass;

        post_dict = dict(self.request.POST);

        event_type = getPostObj(post_dict, 'event_creation_event_type');
        event_name = getPostObj(post_dict, 'event_creation_event_name');
        event_status = getPostObj(post_dict, 'event_creation_event_status');
        event_description = getPostObj(post_dict, 'event_creation_event_description');
        event_location = getPostObj(post_dict, 'event_creation_event_location');
        event_region = getPostObj(post_dict, 'event_creation_event_region');
        event_host = getPostObj(post_dict, 'event_creation_event_host');
        event_school = getPostObj(post_dict, 'event_creation_event_team');
        event_num_race = getPostObj(post_dict, 'event_creation_event_num_race');
        event_num_boat = getPostObj(post_dict, 'event_creation_event_num_boat');
        event_start_date = getPostObj(post_dict, 'event_creation_event_start_date');
        event_end_date = getPostObj(post_dict, 'event_creation_event_end_date');

        try:
            dispatcher = super().populateDispatcher();
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None);
                if action == 'edit':
                    edit(event_creation_id);
                elif action == 'delete':
                    delete(event_creation_id);
            else:
                if action == 'add':
                    add();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request." });

    def rotationGenerator(self, event_team_number, event_boat_number, event_race_number):
        return dict();