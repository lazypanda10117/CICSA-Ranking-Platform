from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class TeamView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = Team;
        self.form_class = TeamForm;
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                team_id = kwargs.pop('id', None);
                team = self.base_class.objects.get(id=team_id);
            else:
                team = self.base_class();

            team.team_name = getPostObj(post_dict, 'team_name');
            team.team_school = getPostObj(post_dict, 'team_school');
            team.team_status = getPostObj(post_dict, 'team_status');

            if not action == 'delete':
                team.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=team.id));

            if action == 'delete':
                team.delete();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request." });

### View Generating Functions

    ### Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action');
        element_id = kwargs.pop('element_id');
        field_data_dispatcher = self.populateDispatcher();
        if field_data_dispatcher.get(action):
            field_data = filterDict(getModelObject(self.base_class,id=element_id).__dict__.items(),
                                    self.validation_table['base_form_invalid']);
            return field_data;
        return None;

    def getChoiceData(self):
        choice_data = {};
        choice_data["team_status"] = Choices().getTeamStatusChoices();
        choice_data["team_school"] = Choices().getSchoolChoices();
        return choice_data;

    def getMultiChoiceData(self):
        return None;

    def getSearchElement(self, **kwargs):
        return None;

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = grabValueAsList(field_data);
        return field_data;
