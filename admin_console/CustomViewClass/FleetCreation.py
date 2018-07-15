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
        self.event_activity_type = "race";
        super().__init__(request);

    ### Class Specific Functions
    def setFormPath(self):
        return 'fleet';

    def __rotationGenerator(self, event_team_number, event_boat_number, event_race_number):
        return dict();


    def abstractFormProcess(self, action, **kwargs):
        def add():
            post_dict = dict(self.request.POST);

            event_type = getSinglePostObj(post_dict, 'event_type');
            event_name = getSinglePostObj(post_dict, 'event_name');
            event_status = getSinglePostObj(post_dict, 'event_status');
            event_description = getSinglePostObj(post_dict, 'event_description');
            event_location = getSinglePostObj(post_dict, 'event_location');
            event_region = getSinglePostObj(post_dict, 'event_region');
            event_host = getSinglePostObj(post_dict, 'event_host');
            event_school = getMultiplePostObj(post_dict, 'event_team');
            event_num_race = getSinglePostObj(post_dict, 'event_num_race');
            event_num_boat = getSinglePostObj(post_dict, 'event_num_boat');
            event_start_date = getSinglePostObj(post_dict, 'event_start_date');
            event_end_date = getSinglePostObj(post_dict, 'event_end_date');

            race_tag_dict = dict();
            team_activity_dict = dict();
            #event generation
            event_creation = self.base_class();
            event_creation.event_type = int(event_type);
            event_creation.event_name = event_name;
            event_creation.event_status = event_status;
            event_creation.event_description = event_description;
            event_creation.event_location = event_location;
            event_creation.event_region = int(event_region);
            event_creation.event_host = int(event_host);
            event_creation.event_boat_number = int(event_num_boat);
            event_creation.event_race_number = int(event_num_race);
            event_creation.event_start_date = event_start_date;
            event_creation.event_end_date = event_end_date;
            event_creation.event_team_number = len(event_school);
            event_creation.event_rotation_detail = self.__rotationGenerator(
                event_creation.event_team_number, event_creation.event_boat_number, event_creation.event_race_number);
            event_creation.save();
            loghelper(self.request, 'admin',
                      logQueryMaker(self.base_class, action.title(), id=event_creation.id))

            #event tag generation
            for tag in self.event_race_tag:
                event_tag = self.assoc_class_tag();
                event_tag.event_tag_event_id = event_creation.id;
                event_tag.event_tag_name = tag;
                event_tag.save();
                race_tag_dict[tag] = event_tag.id;
                loghelper(self.request, 'admin',
                          logQueryMaker(self.assoc_class_tag, action.title(), id=event_tag.id));

            for school_id in event_school:
                school = self.assoc_class_school.objects.get(id=school_id);
                #summary generation
                summary = self.assoc_class_summary();
                summary.summary_event_parent = event_creation.id;
                summary.summary_event_school = school_id;
                summary.save();
                loghelper(self.request, 'admin',
                          logQueryMaker(self.assoc_class_summary, action.title(), id=summary.id));
                #team generation
                for index, suffix in enumerate(self.event_team_name_suffix):
                    team = self.assoc_class_team();
                    team_name = str(school.school_default_team_name) + ' ' + suffix;
                    team.team_name = team_name;
                    team.team_school = school_id;
                    team.team_status = "active";
                    team.save();
                    if self.event_race_tag[index] not in team_activity_dict:
                        team_activity_dict[self.event_race_tag[index]] = [];
                    team_activity_dict[self.event_race_tag[index]].append(team.id);
                    loghelper(self.request, 'admin',
                              logQueryMaker(self.assoc_class_team, action.title(), id=team.id));
            for tag, tag_id in race_tag_dict.items():
               for race in range(event_creation.event_race_number):
                    #event activity generation
                    event_activity = self.assoc_class_activity();
                    event_activity.event_activity_event_parent = event_creation.id;
                    event_activity.event_activity_event_tag = tag_id;
                    event_activity.event_activity_name = tag + ' Race ' + str(race+1);
                    event_activity.event_activity_order = race+1;
                    event_activity.event_activity_result = dict();
                    event_activity.event_activity_note = "";
                    event_activity.event_activity_type = self.event_activity_type;
                    event_activity.event_activity_status = "future";
                    event_activity.save();
                    loghelper(self.request, 'admin',
                              logQueryMaker(self.assoc_class_activity, action.title(), id=event_activity.id));
                    for team_id in team_activity_dict[tag]:
                        #event team link generation
                        event_team = self.assoc_class_team_link();
                        event_team.event_team_event_activity_id = event_activity.id;
                        event_team.event_team_id = team_id;
                        event_team.save();
                        loghelper(self.request, 'admin',
                                  logQueryMaker(self.assoc_class_team_link, action.title(), id=event_team.id));

        def edit(key):
            pass;

        def delete(key):
            pass;

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