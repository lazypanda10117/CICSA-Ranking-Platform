from django import forms
from django.utils import timezone

from cicsa_ranking.models import Event
from api.authentication import AuthenticationGuardType
from misc.CustomElements import Dispatcher
from panel.component.CustomElements import CustomForm
from panel.module.ModuleRegistry import ModuleRegistry
from panel.module.base.structure.data_app.CoreComponents import CoreDataComponent
from panel.module.base.structure.data_app.CoreComponents import CoreDataTableView
from panel.module.base.structure.data_app.CoreComponents import CoreDataActionProcess
from panel.module.base.structure.data_app.CoreComponents import CoreDataFormView
from panel.module.base.structure.data_app.constants import ComponentType


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
        pass

    def getRowContent(self, model_object):
        pass


class FleetRaceForm(CoreDataFormView):
    def _setValidationSet(self):
        return {'_state', 'id', 'event_team_number', 'event_school_ids', 'event_rotation_detail', 'event_create_time'}

    def _setFormObject(self):
        return FleetRaceFormObject

    def getFieldData(self, **kwargs):
        pass


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
