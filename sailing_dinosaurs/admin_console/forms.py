from .models import School, Season, Region, EventType, ScoreMapping, Account
from django import forms

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'

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
