from .models import School, Season, Region, EventType, ScoreMapping, Account, Log
from django import forms

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
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(max_length=200)
    region = forms.IntegerField()
    status = forms.CharField(max_length=50)
    season_score = forms.FloatField()