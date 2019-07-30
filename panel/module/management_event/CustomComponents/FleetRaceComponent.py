from django import forms
from django.utils import timezone

from api import EventTypeAPI
from api import EventAPI
from cicsa_ranking.models import Event
from cicsa_ranking.models import EventType
from api.authentication import AuthenticationGuardType
from misc.CustomElements import Dispatcher
from misc.CustomFunctions import MiscFunctions
from panel.component.CustomElements import CustomForm, Choices
from panel.module.ModuleRegistry import ModuleRegistry
from panel.module.base.structure.data_app.CoreComponents import CoreDataComponent
from panel.module.base.structure.data_app.CoreComponents import CoreDataTableView
from panel.module.base.structure.data_app.CoreComponents import CoreDataActionProcess
from panel.module.base.structure.data_app.CoreComponents import CoreDataFormView
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
            )
        ).getChoiceData()
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
        choice_data['event_type'] = (lambda event_type: (event_type.id, event_type.event_type_name))(
            EventTypeAPI(self.request).getSelf(event_type_name=EventType.FLEET_RACE)
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
    def _add(self, **kwargs):
        pass

    def _edit(self, **kwargs):
        pass

    def _delete(self, **kwargs):
        pass
