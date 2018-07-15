import hashlib, random, string

from .AbstractCustomClass import AbstractCustomClass
from ..HelperClass import *
from ..generalFunctions import *

from ..models import *
from ..forms import *

class MemberGroupView(AbstractCustomClass):

### Constructor <-> AbstractCustomClass

    def __init__(self, request):
        self.base_class = MemberGroup;
        self.form_class = MemberGroupForm;
        self.assoc_class_member = Member;
        self.search_name = ['member0', 'member1'];
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'member_group_member_ids'},
        };
        super().__init__(request, self.base_class, self.validation_table);

### View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST);
            dispatcher = super().populateDispatcher();

            if dispatcher.get(action):
                member_group_id = kwargs.pop('id', None);
                member_group = self.base_class.objects.get(id=member_group_id);
            else:
                member_group = self.base_class();

            member_group.member_group_name = getSinglePostObj(post_dict, 'member_group_name');
            member_group.member_group_school = getSinglePostObj(post_dict, 'member_group_school');
            member_group.member_group_member_ids = [getSinglePostObj(post_dict, name + "_result") for name in self.search_name]

            if not action == 'delete':
                member_group.save();

            loghelper(self.request, 'admin', logQueryMaker(self.base_class, action.title(), id=member_group.id));

            if action == 'delete':
                member_group.delete();
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
        choice_data = dict();
        choice_data["member_group_school"] = Choices().getSchoolChoices();
        return choice_data;

    def getDBMap(self, data):
        db_map = dict();
        db_map['member_group_member_ids'] = [
            DBMap().getMap(self.assoc_class_member, data['member_group_member_ids'][i], 'member_name')
            for i in range(len(data['member_group_member_ids']))
        ];
        return db_map;

    def getMultiChoiceData(self):
        return None;

    def getSearchElement(self, **kwargs):
        def getSearchDefault(id):
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None;
            if element_id:
                member_group = getModelObject(self.base_class, id=element_id);
                if member_group.member_group_member_ids is not None:
                    member = getModelObject(self.assoc_class_member, id=member_group.member_group_member_ids[id]);
                    return member.id, member.member_name + ' (' + member.member_email + ')';
            return None, None;
        return [
                    SearchElement(self.search_name[i], 'Member '+ str(i), 'Member', '', 'member_name', 'member_email',
                                  getSearchDefault(i)) for i in range(len(self.search_name))
                ];

    ### Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if not field.name in self.validation_table['base_table_invalid']];

    def getTableRowContent(self, content):
        field_data = filterDict(getModelObject(self.base_class, id=content.id).__dict__.items(),
                                                self.validation_table['base_table_invalid']);
        field_data = self.updateChoiceAsValue(field_data, self.getChoiceData());
        field_data = self.updateDBMapAsValue(field_data, self.getDBMap(field_data));
        field_data = grabValueAsList(field_data);
        return field_data;
