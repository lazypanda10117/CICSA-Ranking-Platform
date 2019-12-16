from cicsa_ranking.models import Event, EventTag
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import DBMap, SearchElement
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class EventTagView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = EventTag
        self.assoc_class_event = Event
        self.search_name = ['event_tag_linked_event']
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_tag_event_id'},
        }
        super().__init__(request, self.base_class, self.validation_table)


# View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        try:
            post_dict = dict(self.request.POST)
            dispatcher = super().populateDispatcher()

            if dispatcher.get(action):
                event_tag_id = kwargs.pop('id', None)
                event_tag = self.useAPI(self.base_class).editSelf(id=event_tag_id)
            else:
                event_tag = self.base_class()

            event_tag.event_tag_event_id = [RequestFunctions.getSingleRequestObj(
                post_dict, name + "_result") for name in self.search_name][0]
            event_tag.event_tag_name = RequestFunctions.getSingleRequestObj(post_dict, 'event_tag_name')

            if not action == 'delete':
                event_tag.save()

            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=event_tag.id))

            if action == 'delete':
                event_tag.delete()
        except Exception:
            print({"Error": "Cannot Process " + action.title() + " Request."})

# View Generating Functions

    # Form Generating Functions
    def getFieldData(self, **kwargs):
        action = kwargs.pop('action')
        element_id = kwargs.pop('element_id')
        field_data_dispatcher = self.populateDispatcher()
        if field_data_dispatcher.get(action):
            field_data = MiscFunctions.filterDict(
                self.useAPI(self.base_class).getSelf(id=element_id).__dict__.items(),
                self.validation_table['base_form_invalid']
            )
            return field_data
        return None

    def getChoiceData(self):
        return None

    def getDBMap(self, data):
        db_map = dict()
        db_map['event_tag_event_id'] = DBMap().getMap(self.assoc_class_event,
                                                      data['event_tag_event_id'], 'event_name')
        return db_map

    def getMultiChoiceData(self):
        return None

    def getSearchElement(self, **kwargs):
        def getSearchDefault(id):
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None
            if element_id:
                event_tag = self.useAPI(self.base_class).getSelf(id=element_id)
                if event_tag.event_tag_event_id is not None:
                    linked_event = self.useAPI(self.assoc_class_event).getSelf(id=event_tag.event_tag_event_id)
                    return linked_event.id, linked_event.event_name
            return None, None
        return [
                    SearchElement(self.search_name[i], 'Linked Event', 'Event', '', 'event_name', '',
                                  getSearchDefault(i)) for i in range(len(self.search_name))
                ]

    # Table Generating Functions
    def getTableSpecificHeader(self):
        return [field.name for field in self.base_class._meta.get_fields()
                if field.name not in self.validation_table['base_table_invalid']]

    def getTableRowContent(self, content):
        field_data = MiscFunctions.filterDict(self.useAPI(self.base_class).getSelf(id=content.id).__dict__.items(),
                                              self.validation_table['base_table_invalid'])
        field_data = self.updateDBMapAsValue(field_data, self.getDBMap(field_data))
        field_data = MiscFunctions.grabValueAsList(field_data)
        return field_data
