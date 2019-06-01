from cicsa_ranking.models import Event, EventActivity, EventTag, EventTeam
from .AbstractCustomClass import AbstractCustomClass
from panel.component.CustomElements import Choices, DBMap, SearchElement
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class EventActivityView(AbstractCustomClass):
    def __init__(self, request):
        self.base_class = EventActivity
        self.assoc_class_event = Event
        self.assoc_class_event_tag = EventTag
        self.assoc_class_team_link = EventTeam
        self.search_name = ['event_activity_event_parent', 'evnet_activity_event_tag']
        self.validation_table = {
            'base_table_invalid': {'_state'},
            'base_form_invalid': {'_state', 'id', 'event_activity_event_parent', 'event_activity_event_tag'},
        }
        super().__init__(request, self.base_class, self.validation_table)

    @staticmethod
    def __fleetRotationUpdater(tag_id, team_num, action, rotation):
        def updateRotationArray(action, array):
            if action == 'add':
                if len(array) % 2 == 0:
                    array.append(MiscFunctions.modAdd(array[len(array)-1]-1, 2, team_num))
                else:
                    array.append(array[len(array)-1])
                return array
            elif action == 'delete':
                array.pop()
                return array
        new_rotation = rotation
        new_rotation[tag_id] = {team_id: updateRotationArray(action, team_rot)
                                for team_id, team_rot in rotation[str(tag_id)].items()}
        return new_rotation

    @staticmethod
    def __teamRotationUpdater():
        return dict()

# View Process Functions

    def abstractFormProcess(self, action, **kwargs):
        def add():
            event_api = self.useAPI(self.assoc_class_event)
            event_activity = self.base_class()
            event_activity.event_activity_event_parent = int(
                [RequestFunctions.getSinglePostObj(post_dict, self.search_name[0] + "_result")][0])
            event_activity.event_activity_event_tag = int(
                [RequestFunctions.getSinglePostObj(post_dict, self.search_name[1] + "_result")][0])
            event_activity.event_activity_name = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_name')
            event_activity.event_activity_order = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_order')
            event_activity.event_activity_result = MiscFunctions.jsonLoadCatch(
                RequestFunctions.getSinglePostObj(post_dict, 'event_activity_result'))
            event_activity.event_activity_type = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_type')
            event_activity.event_activity_note = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_note')
            event_activity.event_activity_status = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_status')
            event_activity.save()

            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=event_activity.id))

            teams = event_api.getEventCascadeTeams(event_activity.event_activity_event_parent)
            matching_teams = list(filter(lambda x: x.team_tag_id == event_activity.event_activity_event_tag, teams))
            for team in matching_teams:
                event_team = self.assoc_class_team_link()
                event_team.event_team_event_activity_id = event_activity.id
                event_team.event_team_id = team.id
                event_team.save()
                LogFunctions.generateLog(
                    self.request, 'admin', LogFunctions.makeLogQuery(
                        self.assoc_class_team_link, action.title(), id=event_team.id))

            event = event_api.getSelf(id=event_activity.event_activity_event_parent)
            event_type = int(event.event_type)
            event_team_num = int(event.event_team_number)
            event_rotation = event.event_rotation_detail
            event_tag = event_activity.event_activity_event_tag
            new_rotation = {}
            if event_type == 1:
                new_rotation = self.__fleetRotationUpdater(event_tag, event_team_num, 'add', event_rotation)
            elif event_type == 2:
                new_rotation = self.__teamRotationUpdater()
            event.event_rotation_detail = new_rotation
            event.save()
            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.assoc_class_event, action.title(), id=event.id))

        def edit(key):
            event_activity = self.useAPI(self.base_class).verifySelf(id=key)
            event_activity.event_activity_event_parent = int(
                [RequestFunctions.getSinglePostObj(post_dict, self.search_name[0] + "_result")][0])
            event_activity.event_activity_event_tag = int(
                [RequestFunctions.getSinglePostObj(post_dict, self.search_name[1] + "_result")][0])
            event_activity.event_activity_name = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_name')
            event_activity.event_activity_order = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_order')
            event_activity.event_activity_result = MiscFunctions.jsonLoadCatch(
                RequestFunctions.getSinglePostObj(post_dict, 'event_activity_result'))
            event_activity.event_activity_type = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_type')
            event_activity.event_activity_note = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_note')
            event_activity.event_activity_status = RequestFunctions.getSinglePostObj(post_dict, 'event_activity_status')
            event_activity.save()
            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=event_activity.id))

        def delete(key):
            event_api = self.useAPI(self.assoc_class_event)
            event_activity = self.useAPI(self.base_class).verifySelf(id=key)
            event_team_links = self.useAPI(
                self.assoc_class_team_link
            ).filterSelf(event_team_event_activity_id=event_activity.id)

            for event_team_link in event_team_links:
                LogFunctions.generateLog(
                    self.request, 'admin', LogFunctions.makeLogQuery(
                        self.assoc_class_team_link, action.title(), id=event_team_link.id))
                event_team_link.delete()
            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=event_activity.id))
            event_activity.delete()

            event = event_api.getSelf(id=event_activity.event_activity_event_parent)
            event_type = int(event.event_type)
            event_team_num = int(event.event_team_number)
            event_rotation = event.event_rotation_detail
            event_tag = event_activity.event_activity_event_tag
            new_rotation = {}
            if event_type == 1:
                new_rotation = self.__fleetRotationUpdater(event_tag, event_team_num, 'delete', event_rotation)
            elif event_type == 2:
                new_rotation = self.__teamRotationUpdater()
            event.event_rotation_detail = new_rotation
            event.save()
            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.assoc_class_event, action.title(), id=event.id))

        try:
            post_dict = dict(self.request.POST)
            dispatcher = super().populateDispatcher()
            if dispatcher.get(action):
                event_activity_id = kwargs.pop('id', None)
                if action == 'edit':
                    edit(event_activity_id)
                elif action == 'delete':
                    delete(event_activity_id)
            else:
                if action == 'add':
                    add()
        except Exception as e:
            print({"Error": "Cannot Process " + action.title() + " Request."})
            print(e)

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
        choice_data['event_activity_type'] = Choices().getEventActivityTypeChoices()
        choice_data['event_activity_status'] = Choices().getEventStatusChoices()
        return choice_data

    def getDBMap(self, data):
        db_map = dict()
        db_map['event_activity_event_parent'] = DBMap().getMap(self.assoc_class_event,
                                                               data['event_activity_event_parent'], 'event_name')
        db_map['event_activity_event_tag'] = DBMap().getMap(self.assoc_class_event_tag,
                                                            data['event_activity_event_tag'], 'event_tag_name')
        return db_map

    def getMultiChoiceData(self):
        return None

    def getSearchElement(self, **kwargs):
        element_id = kwargs['element_id'] if 'element_id' in kwargs else None

        def searchDefaultAbstract0():
            if element_id:
                event_activity = self.useAPI(self.base_class).getSelf(id=element_id)
                if event_activity.event_activity_event_parent is not None:
                    event_parent = self.useAPI(
                        self.assoc_class_event
                    ).getSelf(id=event_activity.event_activity_event_parent)
                    return event_parent
            return None

        def getSearchDefault0():
            return (
                lambda x: (None, None) if x is None else (
                    x.id, x.event_name + ' (' + str(x.event_host) + ')'
                )
            )(searchDefaultAbstract0())

        def getSearchDefault1():
            element_id = kwargs['element_id'] if 'element_id' in kwargs else None
            if element_id:
                event_activity = self.useAPI(self.base_class).getSelf(id=element_id)
                if event_activity.event_activity_event_parent is not None:
                    event_tag = self.useAPI(
                        self.assoc_class_event_tag
                    ).getSelf(id=event_activity.event_activity_event_tag)
                    return event_tag.id, event_tag.event_tag_name + ' (' + str(event_tag.event_tag_event_id) + ')'
            return None, None

        def getSearchKeyDict(field_name):
            return (lambda x: x if x is None else {field_name: x.id})(searchDefaultAbstract0())

        return [
                    SearchElement(self.search_name[0], 'Event Activity Event Parent (Unalterable)',
                                  'Event', getSearchKeyDict("id"), 'event_name', 'id', getSearchDefault0()),
                    SearchElement(self.search_name[1], 'Event Activity Event Tag',
                                  'EventTag', getSearchKeyDict("event_tag_event_id"), 'event_tag_name',
                                  'event_tag_event_id', getSearchDefault1())
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
