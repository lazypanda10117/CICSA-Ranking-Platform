from cicsa_ranking.models import Member
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class MemberView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = Member
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
                member_id = kwargs.pop('id', None)
                member = self.useAPI(self.base_class).verifySelf(id=member_id)
            else:
                member = self.base_class()

            member.member_name = RequestFunctions.getSinglePostObj(post_dict, 'member_name')
            member.member_school = RequestFunctions.getSinglePostObj(post_dict, 'member_school')
            member.member_email = RequestFunctions.getSinglePostObj(post_dict, 'member_email')
            member.member_status = RequestFunctions.getSinglePostObj(post_dict, 'member_status')

            if not action == 'delete':
                member.save()

            LogFunctions.loghelper(
                self.request, 'admin', LogFunctions.logQueryMaker(self.base_class, action.title(), id=member.id))

            if action == 'delete':
                member.delete()
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
        choice_data["member_status"] = Choices().getStatusChoices()
        choice_data["member_school"] = Choices().getSchoolChoices()
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
