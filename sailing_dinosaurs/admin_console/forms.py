from .models import *
from django import forms

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['school_name', 'school_region', 'school_status', 'school_season_score']

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        exclude = []

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        exclude = []

class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        exclude = []

class ScoreMappingForm(forms.ModelForm):
    class Meta:
        model = ScoreMapping
        exclude = []
