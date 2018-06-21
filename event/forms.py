from django import forms

class EventCreationForm(forms.Form):
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