from .models import *
from django import forms

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['school_name', 'school_region', 'school_status', 'school_season_score']