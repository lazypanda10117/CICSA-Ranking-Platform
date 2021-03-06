from cicsa_ranking.models import Member, MemberGroup, School
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices, DBMap, SearchElement
from misc.CustomFunctions import MiscFunctions, ModelFunctions, RequestFunctions, LogFunctions


class MemberGroupView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = MemberGroup
        self.assoc_class_school = School
        self.assoc_class_member = Member
        self.search_name = ['member_group_member_ids_0', 'member_group_member_ids_1']
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'member_group_member_ids'},
        }
        super().__init__(request, self.base_class, self.validation_table)

# View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST)
            dispatcher = super().populateDispatcher()

            if dispatcher.get(action):
                member_group_id = kwargs.pop('id', None)
                member_group = self.useAPI(self.base_class).editSelf(id=member_group_id)
            else:
                member_group = self.base_class()

            member_group.member_group_school = RequestFunctions.getSingleRequestObj(post_dict, 'member_group_school')
            member_group.member_group_member_ids = [RequestFunctions.getSingleRequestObj(post_dict, name + "_result")
                                                    for name in self.search_name]
            if action == 'add':
                member_group.member_group_name = ModelFunctions.getModelObject(
                    self.assoc_class_school,
                    id=member_group.member_group_school
                ).school_name + ' - ' + RequestFunctions.getSingleRequestObj(
                    post_dict, 'member_group_name'
                )
            elif action == 'edit':
                member_group.member_group_name = RequestFunctions.getSingleRequestObj(post_dict, 'member_group_name')

            member_group.save()

            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=member_group.id))

            if action == 'delete':
                member_group.delete()
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
        choice_data["member_group_school"] = Choices().getSchoolChoices()
        return choice_data

    def getDBMap(self, data):
        db_map = dict()
        db_map['member_group_member_ids'] = [
            DBMap().getMap(self.assoc_class_member, data['member_group_member_ids'][i], 'member_name')
            for i in range(len(data['member_group_member_ids']))
        ]
        return db_map

    def getMultiChoiceData(self):
        return None

    def getSearchElement(self, **kwargs):
        def getSearchDefault(id):
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None
            if element_id:
                member_group = self.useAPI(self.base_class).getSelf(id=element_id)
                if member_group.member_group_member_ids is not None:
                    member = self.useAPI(self.assoc_class_member).getSelf(id=member_group.member_group_member_ids[id])
                    return member.id, member.member_name + ' (' + member.member_email + ')'
            return None, None
        return [
                    SearchElement(
                        self.search_name[i],
                        'Member ' + str(i),
                        'Member',
                        None,
                        'member_name',
                        'member_email',
                        getSearchDefault(i)
                    ) for i in range(len(self.search_name))
                ]

    # Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if field.name not in self.validation_table['base_table_invalid']]

    def getTableRowContent(self, content):
        field_data = MiscFunctions.filterDict(self.useAPI(self.base_class).getSelf(id=content.id).__dict__.items(),
                                              self.validation_table['base_table_invalid'])
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData())
        field_data = self.updateDBMapAsValue(field_data, self.getDBMap(field_data))
        field_data = MiscFunctions.grabValueAsList(field_data)
        return field_data
