from django import forms
from .generalFunctions import *
from .models import Season, Region, EventType, ScoreMapping, Log


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = '__all__'


class ScoreMappingForm(forms.ModelForm):
    class Meta:
        model = ScoreMapping
        fields = '__all__'


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = '__all__'


class AccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    account_type = forms.ChoiceField(choices=[]);
    account_email = forms.EmailField();
    account_password = forms.CharField(max_length=200);
    account_status = forms.ChoiceField(choices=[]);
    account_linked_id = forms.IntegerField(initial=-1);


class SchoolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    school_name = forms.CharField(max_length=200);
    school_region = forms.ChoiceField(choices=[]);
    school_status = forms.ChoiceField(choices=[]);
    school_season_score = forms.FloatField(initial=0);
    school_default_team_name = forms.CharField(max_length=200);
    account_email = forms.EmailField();
    account_password = forms.CharField(max_length=200);


class TeamForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    team_name = forms.CharField(max_length=200);
    team_school = forms.ChoiceField(choices=[]);
    team_status = forms.ChoiceField(choices=[]);


class MemberForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    member_name = forms.CharField(max_length=200);
    member_school = forms.ChoiceField(choices=[]);
    member_email = forms.EmailField(required=False);
    member_status = forms.ChoiceField(choices=[]);


class MemberGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    member_group_name = forms.CharField(max_length=200);
    member_group_school = forms.ChoiceField(choices=[]);


class EventManagementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        self.multi_choice_data = (lambda x: x if x else {})(noneCatcher('multi_choice_data', self.data));
        for key, value in self.multi_choice_data.items():
            self.fields[key] = forms.MultipleChoiceField(choices=value, widget=forms.CheckboxSelectMultiple);
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    event_type = forms.ChoiceField(choices=[]);
    event_name = forms.CharField(max_length=200);
    event_status = forms.ChoiceField(choices=[]);
    event_description = forms.CharField(max_length=1500, widget=forms.Textarea, required=False);
    event_location = forms.CharField(max_length=1000);
    event_season = forms.ChoiceField(choices=[]);
    event_region = forms.ChoiceField(choices=[]);
    event_host = forms.ChoiceField(choices=[]);
    event_team = forms.MultipleChoiceField(choices=[]);
    event_race_number = forms.IntegerField();
    event_boat_rotation_name = forms.CharField(max_length=2000);
    event_start_date = forms.DateField(initial=timezone.now(), widget=forms.DateInput(format='%Y-%m-%d'));
    event_end_date = forms.DateField(initial=timezone.now(), widget=forms.DateInput(format='%Y-%m-%d'));


class EventForm(EventManagementForm):
    event_rotation_detail = forms.CharField(max_length=5000, widget=forms.Textarea);


class SummaryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    summary_event_school = forms.ChoiceField(choices=[]);
    summary_event_ranking = forms.IntegerField(initial=0);
    summary_event_override_ranking = forms.IntegerField(initial=0);
    summary_event_score = forms.FloatField(initial=0.0);


class EventTeamForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    event_team_id = forms.IntegerField();
    event_team_event_activity_id = forms.IntegerField();


class EventTagForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    event_tag_name = forms.CharField(max_length=200);


class EventActivityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else {})(noneCatcher('field_data', self.data));
        self.choice_data = (lambda x: x if x else {})(noneCatcher('choice_data', self.data));
        for key, value in self.choice_data.items():
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data.items():
            self.fields[key].initial = value;

    event_activity_name = forms.CharField(max_length=100);
    event_activity_order = forms.IntegerField(initial=1);
    event_activity_result = forms.CharField(max_length=1500, widget=forms.Textarea, required=False);  # json
    event_activity_type = forms.ChoiceField(choices=[]);
    event_activity_note = forms.CharField(max_length=1500, required=False);
    event_activity_status = forms.CharField(max_length=50);