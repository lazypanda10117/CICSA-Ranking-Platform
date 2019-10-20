import random
from misc.CustomFunctions import LogFunctions
from misc.CustomFunctions import MiscFunctions
from misc.CustomFunctions import ModelFunctions
from misc.CustomFunctions import RequestFunctions
from .EventManagement import EventManagementView
from cicsa_ranking.models import EventActivity
from cicsa_ranking.models import Team
from cicsa_ranking.models import School
from cicsa_ranking.models import EventTeam
from cicsa_ranking.models import EventTag
from cicsa_ranking.models import EventType
from cicsa_ranking.models import Summary
from cicsa_ranking.models import Season


class FleetManagementView(EventManagementView):
    def __init__(self, request):
        self.event_type = 'fleet race'
        super().__init__(request)
        self.assoc_class_activity = EventActivity
        self.assoc_class_team = Team
        self.assoc_class_school = School
        self.assoc_class_team_link = EventTeam
        self.assoc_class_tag = EventTag
        self.assoc_class_type = EventType
        self.assoc_class_summary = Summary
        self.assoc_class_season = Season

        self.event_race_tag = [EventTag.DEFAULT_EVENT_TAGS + ' {}'.format(MiscFunctions.getAlphabet(i)) for i in range(2)]
        self.event_team_name_suffix = [Team.TEAM_NAME_SUFFIX + ' {}'.format(MiscFunctions.getAlphabet(i)) for i in range(2)]
        self.event_activity_type = EventActivity.ACTIVITY_TYPE_RACE

    # Class Specific Functions
    def getChoiceData(self):
        choice_data = super().getChoiceData()
        choice_data['event_type'] = tuple(
            [(lambda x: (x.id, x.event_type_name))
             (self.useAPI(self.assoc_class_type).getSelf(event_type_name=self.event_type))])
        return choice_data

    def setFormPath(self):
        return self.event_type

    def __rotationGenerator(self, tag_dict, team_dict, event_race_number, event_team_number):
        rand_array = random.sample(range(1, event_team_number + 1), event_team_number)
        result_dict = dict()
        for shift, tag in enumerate(tag_dict):
            team_sequence = dict()
            for team_num, team_id in enumerate(team_dict[tag]):
                team_sequence[team_id] = [
                    MiscFunctions.modAdd(
                        rand_array[team_num] + shift, (race - race % 2),
                        event_team_number
                    )
                    for race in range(event_race_number)
                ]
            result_dict[tag_dict[tag]] = team_sequence
        return result_dict

    def abstractFormProcess(self, action, **kwargs):
        def add():
            post_dict = dict(self.request.POST)

            event_type = RequestFunctions.getSinglePostObj(post_dict, 'event_type')
            event_class = RequestFunctions.getSinglePostObj(post_dict, 'event_class')
            event_name = RequestFunctions.getSinglePostObj(post_dict, 'event_name')
            event_status = RequestFunctions.getSinglePostObj(post_dict, 'event_status')
            event_description = RequestFunctions.getSinglePostObj(post_dict, 'event_description')
            event_location = RequestFunctions.getSinglePostObj(post_dict, 'event_location')
            event_season = RequestFunctions.getSinglePostObj(post_dict, 'event_season')
            event_region = RequestFunctions.getSinglePostObj(post_dict, 'event_region')
            event_host = RequestFunctions.getSinglePostObj(post_dict, 'event_host')
            event_school = RequestFunctions.getMultiplePostObj(post_dict, 'event_team')
            event_race_number = RequestFunctions.getSinglePostObj(post_dict, 'event_race_number')
            event_boat_rotation_name = RequestFunctions.getSinglePostObj(post_dict, 'event_boat_rotation_name')
            event_start_date = RequestFunctions.getSinglePostObj(post_dict, 'event_start_date')
            event_end_date = RequestFunctions.getSinglePostObj(post_dict, 'event_end_date')

            race_tag_dict = dict()
            team_activity_dict = dict()
            # event generation
            event_creation = self.base_class()
            event_creation.event_type = int(event_type)
            event_creation.event_class = int(event_class)
            event_creation.event_name = event_name
            event_creation.event_status = event_status
            event_creation.event_description = event_description
            event_creation.event_location = event_location
            event_creation.event_season = event_season
            event_creation.event_region = int(event_region)
            event_creation.event_host = int(event_host)
            event_creation.event_boat_rotation_name = event_boat_rotation_name
            event_creation.event_race_number = int(event_race_number)
            event_creation.event_start_date = event_start_date
            event_creation.event_end_date = event_end_date
            event_creation.event_team_number = len(event_school)
            event_creation.event_school_ids = event_school
            event_creation.event_rotation_detail = {}
            event_creation.save()

            # event tag generation
            for tag in self.event_race_tag:
                event_tag = self.assoc_class_tag()
                event_tag.event_tag_event_id = event_creation.id
                event_tag.event_tag_name = tag
                event_tag.save()
                race_tag_dict[tag] = event_tag.id
                LogFunctions.generateLog(self.request, 'admin',
                                         LogFunctions.makeLogQuery(
                                           self.assoc_class_tag, action.title(), id=event_tag.id))

            for school_id in event_school:
                # NOTE: not sure if using api here will cause error
                school = ModelFunctions.getModelObject(School, id=school_id)
                # summary generation
                summary = self.assoc_class_summary()
                summary.summary_event_parent = event_creation.id
                summary.summary_event_school = school_id
                summary.save()
                LogFunctions.generateLog(self.request, 'admin',
                                         LogFunctions.makeLogQuery(
                                           self.assoc_class_summary, action.title(), id=summary.id))
                # team generation
                for index, suffix in enumerate(self.event_team_name_suffix):
                    team = self.assoc_class_team()
                    team_name = str(school.school_default_team_name) + ' ' + suffix
                    team.team_name = team_name
                    team.team_school = school_id
                    team.team_status = "active"
                    team.team_tag_id = list(race_tag_dict.values())[index]
                    team.save()
                    if self.event_race_tag[index] not in team_activity_dict:
                        team_activity_dict[self.event_race_tag[index]] = []
                    team_activity_dict[self.event_race_tag[index]].append(team.id)
                    LogFunctions.generateLog(self.request, 'admin',
                                             LogFunctions.makeLogQuery(
                                               self.assoc_class_team, action.title(), id=team.id))
            for tag, tag_id in race_tag_dict.items():
                for race in range(event_creation.event_race_number):
                    # event activity generation
                    event_activity = self.assoc_class_activity()
                    event_activity.event_activity_event_parent = event_creation.id
                    event_activity.event_activity_event_tag = tag_id
                    event_activity.event_activity_name = tag + ' Race ' + str(race+1)
                    event_activity.event_activity_order = race + 1
                    event_activity.event_activity_result = dict()
                    event_activity.event_activity_note = ""
                    event_activity.event_activity_type = self.event_activity_type
                    event_activity.event_activity_status = "future"
                    event_activity.save()
                    LogFunctions.generateLog(self.request, 'admin',
                                             LogFunctions.makeLogQuery(
                                               self.assoc_class_activity, action.title(), id=event_activity.id))
                    for team_id in team_activity_dict[tag]:
                        # event team link generation
                        event_team = self.assoc_class_team_link()
                        event_team.event_team_event_activity_id = event_activity.id
                        event_team.event_team_id = team_id
                        event_team.save()
                        LogFunctions.generateLog(self.request, 'admin',
                                                 LogFunctions.makeLogQuery(
                                                   self.assoc_class_team_link, action.title(), id=event_team.id))

            event_creation.event_rotation_detail = self.__rotationGenerator(
                race_tag_dict, team_activity_dict, event_creation.event_race_number, event_creation.event_team_number)
            event_creation.save()
            LogFunctions.generateLog(self.request, 'admin',
                                     LogFunctions.makeLogQuery(self.base_class, action.title(), id=event_creation.id))

        def edit(key):
            delete(key)
            add()

        def delete(key):
            event_api = self.useAPI(self.base_class)
            event_activity_api = self.useAPI(self.assoc_class_activity)
            summary_api = self.useAPI(self.assoc_class_summary)
            event_team_api = self.useAPI(self.assoc_class_team_link)
            event_tag_api = self.useAPI(self.assoc_class_tag)
            event = event_api.verifySelf(id=key)
            event_activities = event_activity_api.filterSelf(event_activity_event_parent=event.id)
            event_summaries = summary_api.filterSelf(summary_event_parent=event.id)

            event_tags = event_tag_api.filterSelf(event_tag_event_id=event.id)
            event_teams = event_api.getEventCascadeTeams(event.id)
            event_team_links = [event_team_api.filterSelf(event_team_event_activity_id=activity.id)
                                for activity in event_activities]

            for team in event_teams:
                LogFunctions.generateLog(self.request, 'admin',
                                         LogFunctions.makeLogQuery(self.assoc_class_team, action.title(), id=team.id))
                team.delete()
            for tag in event_tags:
                LogFunctions.generateLog(self.request, 'admin',
                                         LogFunctions.makeLogQuery(self.assoc_class_tag, action.title(), id=tag.id))
                tag.delete()
            for summary in event_summaries:
                LogFunctions.generateLog(self.request, 'admin',
                                         LogFunctions.makeLogQuery(
                                           self.assoc_class_summary, action.title(), id=summary.id))
                summary.delete()

            for activity in event_activities:
                LogFunctions.generateLog(self.request, 'admin',
                                         LogFunctions.makeLogQuery(
                                           self.assoc_class_activity, action.title(), id=activity.id))
                activity.delete()
            for team_links in event_team_links:
                for team_link in team_links:
                    LogFunctions.generateLog(self.request, 'admin',
                                             LogFunctions.makeLogQuery(
                                               self.assoc_class_team_link, action.title(), id=team_link.id))
                    team_link.delete()
            LogFunctions.generateLog(self.request, 'admin',
                                     LogFunctions.makeLogQuery(self.base_class, action.title(), id=event.id))
            event.delete()

        try:
            dispatcher = super().populateDispatcher()
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None)
                if action == 'edit':
                    edit(event_creation_id)
                elif action == 'delete':
                    delete(event_creation_id)
            else:
                if action == 'add':
                    add()
        except Exception as e:
            print({"Error": "Cannot Process " + action.title() + " Request."})
            print(e)
