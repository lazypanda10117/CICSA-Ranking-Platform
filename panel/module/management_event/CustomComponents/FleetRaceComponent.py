import random

from django import forms
from django.utils import timezone

from cicsa_ranking.models import Event
from cicsa_ranking.models import EventTeam
from cicsa_ranking.models import EventTag
from cicsa_ranking.models import Summary
from cicsa_ranking.models import EventType
from cicsa_ranking.models import School
from cicsa_ranking.models import Team
from cicsa_ranking.models import EventActivity
from api import EventAPI
from api import EventActivityAPI
from api import EventTagAPI
from api import EventTeamAPI
from api import EventTypeAPI
from api import SummaryAPI
from api.authentication import AuthenticationGuardType
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import MiscFunctions
from misc.CustomFunctions import ModelFunctions
from misc.CustomFunctions import RequestFunctions
from panel.component.CustomElements import Choices
from panel.component.CustomElements import CustomForm
from panel.module.ModuleRegistry import ModuleRegistry
from panel.module.base.structure.data_app.CoreComponents import CoreDataActionProcess
from panel.module.base.structure.data_app.CoreComponents import CoreDataComponent
from panel.module.base.structure.data_app.CoreComponents import CoreDataFormView
from panel.module.base.structure.data_app.CoreComponents import CoreDataTableView
from panel.module.base.structure.data_app.constants import ActionType
from panel.module.base.structure.data_app.constants import ComponentType
from panel.module.base.structure.data_app.utils import MiscUtils


class FleetRaceComponent(CoreDataComponent):
    def _getAppName(self):
        return ModuleRegistry.MANAGEMENT_EVENT

    def _getBaseClass(self):
        return Event

    def _setAssociatedComponentClassDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(ComponentType.TABLE, FleetRaceTable)
        dispatcher.add(ComponentType.FORM, FleetRaceForm)
        dispatcher.add(ComponentType.PROCESS, FleetRaceProcess)
        return dispatcher

    def _getGuardType(self):
        return AuthenticationGuardType.ADMIN_GUARD


class FleetRaceTable(CoreDataTableView):
    def _setValidationSet(self):
        return {'_state', 'id', 'event_rotation_detail', 'event_school_ids', 'event_create_time'}

    def getHeaderContent(self):
        replace_dict = dict(
            event_name='Event',
            event_description='Description',
            event_status="Status",
            event_type='Type',
            event_host='Host',
            event_location='Location',
            event_season='Season',
            event_region='Region',
            event_boat_rotation_name='Sail Numbers',
            event_race_number='Number of Races',
            event_team_number='Number of Teams',
            event_date='Date'
        )
        base_header = [
            field.name for field in self.base_class._meta.get_fields() if field.name not in self.validation_set
        ]
        base_header.remove('event_start_date')
        base_header.remove('event_end_date')
        base_header.append('event_date')
        for index, header in enumerate(base_header):
            base_header[index] = replace_dict[header] if header in replace_dict else header
        additional_header = []
        return base_header + additional_header

    def getRowContent(self, model_object):
        field_data = MiscFunctions.filterDict(
            EventAPI(self.request).getSelf(id=model_object.id).__dict__.items(),
            self.validation_set
        )
        date = '{} to {}'.format(str(field_data['event_start_date']), str(field_data['event_end_date']))
        del field_data['event_start_date']
        del field_data['event_end_date']
        field_data['date'] = date
        field_data = MiscUtils(self.request).updateChoiceAsValue(
            field_data,
            FleetRaceForm(
                self.request,
                self.app_name,
                self.base_class,
                self.mutable,
                self.guard
            ).getChoiceData()
        )
        field_data = MiscFunctions.serializeJSONListData(['event_school_ids', 'event_rotation_detail'], field_data)
        field_data = MiscFunctions.grabValueAsList(field_data)
        return field_data

    def injectTableFilter(self):
        return dict(event_type=EventTypeAPI(self.request).getSelf(event_type_name=EventType.FLEET_RACE).id)


class FleetRaceForm(CoreDataFormView):
    def _setValidationSet(self):
        return {'_state', 'id', 'event_team_number', 'event_school_ids', 'event_rotation_detail', 'event_create_time'}

    def _setFormObject(self):
        return FleetRaceFormObject

    def getFieldData(self, **kwargs):
        action = kwargs.pop('action')
        element_id = kwargs.pop('element_id')
        field_data = dict(event_type=EventType.FLEET_RACE)
        if self.populate_data_dispatcher.get(action):
            raw_data = EventAPI(self.request).editSelf(id=element_id).__dict__
            field_data = MiscFunctions.filterDict(raw_data.items(), self.validation_set)
            field_data['event_team'] = raw_data['event_school_ids']
            field_data = MiscFunctions.serializeJSONListData(['event_school_ids', 'event_rotation_detail'], field_data)
            return field_data
        return field_data

    def getChoiceData(self, **kwargs):
        choice_data = dict()
        choice_data['event_type'] = Choices().getEventTypeChoices()
        choice_data['event_status'] = Choices().getEventStatusChoices()
        choice_data['event_host'] = Choices().getSchoolChoices()
        choice_data['event_season'] = Choices().getSeasonChoices()
        choice_data['event_region'] = Choices().getRegionChoices()
        choice_data['event_type'] = tuple(
            [
                (lambda event_type: (event_type.id, event_type.event_type_name))
                (EventTypeAPI(self.request).getSelf(event_type_name=EventType.FLEET_RACE))
            ]
        )
        return choice_data

    def getMultiChoiceData(self, **kwargs):
        multi_choice_data = dict()
        multi_choice_data['event_team'] = Choices().getSchoolChoices()
        return multi_choice_data


class FleetRaceFormObject(CustomForm):
    event_type = forms.ChoiceField(choices=[])
    event_name = forms.CharField(max_length=200)
    event_status = forms.ChoiceField(choices=[])
    event_description = forms.CharField(max_length=1500, widget=forms.Textarea, required=False)
    event_location = forms.CharField(max_length=1000)
    event_season = forms.ChoiceField(choices=[])
    event_region = forms.ChoiceField(choices=[])
    event_host = forms.ChoiceField(choices=[])
    event_team = forms.MultipleChoiceField(choices=[])
    event_race_number = forms.IntegerField()
    event_boat_rotation_name = forms.CharField(max_length=2000)
    event_start_date = forms.DateField(initial=timezone.now(), widget=forms.DateInput(format='%Y-%m-%d'))
    event_end_date = forms.DateField(initial=timezone.now(), widget=forms.DateInput(format='%Y-%m-%d'))


class FleetRaceProcess(CoreDataActionProcess):
    EVENT_RACE_TAG = ["Fleet A", "Fleet B"]
    EVENT_TEAM_NAME_SUFFIX = ["Team A", "Team B"]

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

    def _add(self, **kwargs):
        post_dict = self.post_data

        event_type = RequestFunctions.getSingleRequestObj(post_dict, 'event_type')
        event_name = RequestFunctions.getSingleRequestObj(post_dict, 'event_name')
        event_status = RequestFunctions.getSingleRequestObj(post_dict, 'event_status')
        event_description = RequestFunctions.getSingleRequestObj(post_dict, 'event_description')
        event_location = RequestFunctions.getSingleRequestObj(post_dict, 'event_location')
        event_season = RequestFunctions.getSingleRequestObj(post_dict, 'event_season')
        event_region = RequestFunctions.getSingleRequestObj(post_dict, 'event_region')
        event_host = RequestFunctions.getSingleRequestObj(post_dict, 'event_host')
        event_school = RequestFunctions.getMultipleRequestObj(post_dict, 'event_team')
        event_race_number = RequestFunctions.getSingleRequestObj(post_dict, 'event_race_number')
        event_boat_rotation_name = RequestFunctions.getSingleRequestObj(post_dict, 'event_boat_rotation_name')
        event_start_date = RequestFunctions.getSingleRequestObj(post_dict, 'event_start_date')
        event_end_date = RequestFunctions.getSingleRequestObj(post_dict, 'event_end_date')

        race_tag_dict = dict()
        team_activity_dict = dict()

        # event generation
        event_creation = self.base_class()
        event_creation.event_type = int(event_type)
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
        event_creation.event_rotation_detail = dict()
        event_creation.save()

        # event tag generation
        for tag in self.EVENT_RACE_TAG:
            event_tag = EventTag()
            event_tag.event_tag_event_id = event_creation.id
            event_tag.event_tag_name = tag
            event_tag.save()
            race_tag_dict[tag] = event_tag.id

        for school_id in event_school:
            # NOTE: Cannot use API here because no permission to get Model.
            school = ModelFunctions.getModelObject(School, id=school_id)
            # summary generation
            summary = Summary()
            summary.summary_event_parent = event_creation.id
            summary.summary_event_school = school_id
            summary.save()

            # team generation
            for index, suffix in enumerate(self.EVENT_TEAM_NAME_SUFFIX):
                team = Team()
                team_name = '{} {}'.format(school.school_default_team_name, suffix)
                team.team_name = team_name
                team.team_school = school_id
                team.team_status = Team.TEAM_STATUS_ACTIVE
                team.team_tag_id = list(race_tag_dict.values())[index]
                team.save()
                if self.EVENT_RACE_TAG[index] not in team_activity_dict:
                    team_activity_dict[self.EVENT_RACE_TAG[index]] = []
                team_activity_dict[self.EVENT_RACE_TAG[index]].append(team.id)


        for tag, tag_id in race_tag_dict.items():
            for race in range(event_creation.event_race_number):
                # event activity generation
                event_activity = EventActivity()
                event_activity.event_activity_event_parent = event_creation.id
                event_activity.event_activity_event_tag = tag_id
                event_activity.event_activity_name = '{} Race {}'.format(tag, str(race + 1))
                event_activity.event_activity_order = race + 1
                event_activity.event_activity_result = dict()
                event_activity.event_activity_note = ""
                event_activity.event_activity_type = EventActivity.EVENT_ACTIVITY_TYPE_RACE
                event_activity.event_activity_status = Event.EVENT_STATUS_PENDING
                event_activity.save()

                for team_id in team_activity_dict[tag]:
                    # event team link generation
                    event_team = EventTeam()
                    event_team.event_team_event_activity_id = event_activity.id
                    event_team.event_team_id = team_id
                    event_team.save()

        event_creation.event_rotation_detail = self.__rotationGenerator(
            race_tag_dict,
            team_activity_dict,
            event_creation.event_race_number,
            event_creation.event_team_number
        )
        event_creation.save()

    def _edit(self, **kwargs):
        self._delete(**kwargs)
        self._add(**kwargs)

    def _delete(self, **kwargs):
        event_id = kwargs.pop('id')

        event = EventAPI(self.request).editSelf(id=event_id)
        event_activities = EventActivityAPI(self.request).filterSelf(event_activity_event_parent=event.id)
        event_summaries = SummaryAPI(self.request).filterSelf(summary_event_parent=event.id)
        event_tags = EventTagAPI(self.request).filterSelf(event_tag_event_id=event.id)
        event_teams = EventAPI(self.request).getEventCascadeTeams(event_id=event.id)
        event_team_links = [
            EventTeamAPI(self.request).filterSelf(event_team_event_activity_id=activity.id)
            for activity in event_activities
        ]

        for team in event_teams:
            team.delete()

        for tag in event_tags:
            tag.delete()

        for summary in event_summaries:
            summary.delete()

        for activity in event_activities:
            activity.delete()

        for team_links in event_team_links:
            for team_link in team_links:
                team_link.delete()

        event.delete()
