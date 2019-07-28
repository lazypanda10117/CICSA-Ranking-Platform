from cicsa_ranking.models import Team
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class TeamView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = Team
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id'},
        }
        super().__init__(request, self.base_class, self.validation_table)

# View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST)
            dispatcher = super().populateDispatcher()

            if dispatcher.get(action):
                team_id = kwargs.pop('id', None)
                team = self.useAPI(self.base_class).verifySelf(id=team_id)
            else:
                team = self.base_class()

            team.team_name = RequestFunctions.getSingleRequestObj(post_dict, 'team_name')
            team.team_school = RequestFunctions.getSingleRequestObj(post_dict, 'team_school')
            team.team_tag_id = RequestFunctions.getSingleRequestObj(post_dict, 'team_tag_id')
            team.team_status = RequestFunctions.getSingleRequestObj(post_dict, 'team_status')

            if not action == 'delete':
                team.save()

            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=team.id))

            if action == 'delete':
                team.delete()
        except Exception:
            print({"Error": "Cannot Process " + action.title() + " Request."})

# View Generating Functions

    # Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action')
        element_id = kwargs.pop('element_id')
        field_data_dispatcher = self.populateDispatcher()
        if field_data_dispatcher.get(action):
            field_data = MiscFunctions.filterDict(self.useAPI(self.base_class).getSelf(id=element_id).__dict__.items(),
                                                  self.validation_table['base_form_invalid'])
            return field_data
        return None

    def getChoiceData(self):
        choice_data = dict()
        choice_data["team_status"] = Choices().getTeamStatusChoices()
        choice_data["team_school"] = Choices().getSchoolChoices()
        return choice_data

    def getDBMap(self, data):
        return None

    def getMultiChoiceData(self):
        return None

    def getSearchElement(self, **kwargs):
        return None

    # Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if field.name not in self.validation_table['base_table_invalid']]

    def getTableRowContent(self, content):
        field_data = MiscFunctions.filterDict(self.useAPI(self.base_class).getSelf(id=content.id).__dict__.items(),
                                              self.validation_table['base_table_invalid'])
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData())
        field_data = MiscFunctions.grabValueAsList(field_data)
        return field_data
