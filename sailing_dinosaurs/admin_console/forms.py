from django import forms
from .generalFunctions import *
from .models import School, Season, Region, EventType, ScoreMapping, Account, Log

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
    account_email = forms.EmailField();
    account_password = forms.CharField(max_length=200);