import json
from django import forms

from cicsa_ranking.models import *
from misc.CustomFunctions import MiscFunctions, ModelFunctions, UrlFunctions


class Button:
    def __init__(self, title, style, redirect):
        self.title = title
        self.style = style
        self.redirect = redirect


class Table:
    def __init__(self, current_class, title):
        self.current_class = current_class
        self.title = title
        self.table_element = ''
        self.table_header = ''
        self.table_content = ''

    def buildTable(self, table_header, table_content, table_element=None):
        self.table_element = table_element
        self.table_header = table_header
        self.table_content = table_content
        return self


class Form:
    def __init__(self, form_path, form_name, form_action, destination, data, special_context):
        self.form_path = form_path
        self.form_name = form_name
        self.form_id = self.getFormID()
        self.form_action = form_action.title()
        self.destination = destination
        self.data = data
        self.special_context = special_context

    def getFormID(self):
        return self.form_name + self.form_path


class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data = kwargs.get('data')
        self.field_data = (lambda x: x if x else {})(MiscFunctions.noneCatcher('field_data', self.data))
        self.choice_data = (lambda x: x if x else {})(MiscFunctions.noneCatcher('choice_data', self.data))
        self.multi_choice_data = (lambda x: x if x else {})(MiscFunctions.noneCatcher('multi_choice_data', self.data))
        for key, value in self.multi_choice_data.items():
            if key in self.fields:
                self.fields[key] = forms.MultipleChoiceField(choices=value, widget=forms.CheckboxSelectMultiple)
        for key, value in self.choice_data.items():
            if key in self.fields:
                value = (('', '-- Select an option --'),) + value
                self.fields[key] = forms.ChoiceField(choices=value)
        for key, value in self.field_data.items():
            if key in self.fields:
                self.fields[key].initial = value


class SearchElement:
    # name = search base name
    # label = the text to display for the search box
    # item = the class to search for
    # key = key dict to search for
    # term = the kwargs to search for
    # help term = an extra to display in the search dropdown to help further distinguish between results

    def __init__(self, name, label, item, key, term, help_term, value_tuple):
        self.name = name
        self.label = label
        self.item = self.stringify(item)
        self.key = self.stringify(key)
        self.term = self.stringify(term)
        self.help_term = self.stringify(help_term)
        self.default_value = value_tuple[0]
        self.value = value_tuple[1]

    @staticmethod
    def stringify(text):
        return json.dumps(text)


class Choices:
    @staticmethod
    def getSeasonChoices():
        SEASON_CHOICES = tuple([(value.id, value.season_name) for value in ModelFunctions.filterModelObject(Season)])
        return SEASON_CHOICES

    @staticmethod
    def getRegionChoices():
        REGION_CHOICES = tuple([(value.id, value.region_name) for value in ModelFunctions.filterModelObject(Region)])
        return REGION_CHOICES

    @staticmethod
    def getSchoolChoices():
        SCHOOL_CHOICES = tuple([
            (value.id, value.school_name) for value in ModelFunctions.filterModelObject(School).order_by('school_name')
        ])
        return SCHOOL_CHOICES

    @staticmethod
    def getEventTypeChoices():
        EVENT_TYPE_CHOICES = tuple(
            [(value.id, value.event_type_name) for value in ModelFunctions.filterModelObject(EventType)])
        return EVENT_TYPE_CHOICES

    @staticmethod
    def getScoreMapChoices():
        SCORE_MAP_CHOICES = tuple(
            [(value.id, value.score_name) for value in ModelFunctions.filterModelObject(ScoreMapping)])
        return SCORE_MAP_CHOICES

    @staticmethod
    def getEventStatusChoices():
        EVENT_STATUS_CHOICES = (
            ("future", "Future Event"),
            ("running", "Ongoing Event"),
            ("done", "Completed Event")
        )
        return EVENT_STATUS_CHOICES

    @staticmethod
    def getEventActivityTypeChoices():
        EVENT_ACTIVITY_TYPE_CHOICES = (
            ("race", "Race"),
            ("other", "Other")
        )
        return EVENT_ACTIVITY_TYPE_CHOICES

    @staticmethod
    def getTeamStatusChoices():
        TEAM_STATUS_CHOICES = (
            ("active", "Active"),
            ("dormant", "Dormant"),
            ("hidden", "Hidden")
        )
        return TEAM_STATUS_CHOICES

    @staticmethod
    def getStatusChoices():
        STATUS_CHOICES = (
            ("active", "Active"),
            ("dormant", "Dormant"),
            ("hidden", "Hidden")
        )
        return STATUS_CHOICES

    @staticmethod
    def getAccountTypeChocies():
        ACCOUNT_TYPE_CHOICES = (
            ("admin", "Admin"),
            ("school", "School")
        )
        return ACCOUNT_TYPE_CHOICES


class DBMap:
    @staticmethod
    # NOTE: potential error if use API, so will leave this as is right now
    def getMap(query_class, query_id, target_field):
        result =  ModelFunctions.getModelObject(query_class, id=query_id)
        if result is not None:
            return MiscFunctions.noneCatcher(target_field, result.__dict__)
        return 'Link Broken'
