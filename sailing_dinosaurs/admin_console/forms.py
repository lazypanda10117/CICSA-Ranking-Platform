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

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = '__all__'


class SchoolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        data = kwargs.pop('data', None);
        self.field_data = (lambda x: x if x else [])(noneCatcher('field_data', data));
        self.choice_data = (lambda x: x if x else [])(noneCatcher('choice_data', data));
        for key, value in self.field_data:
            self.fields[key] = forms.ChoiceField(choices=value);
        for key, value in self.field_data:
            self.fields[key].initials = value;

    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(max_length=200)
    region = forms.ChoiceField(choices=[(1,"hi")]);
    status = forms.ChoiceField(choices=[]);
    season_score = forms.FloatField()