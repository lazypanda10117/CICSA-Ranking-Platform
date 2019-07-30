from cicsa_ranking.models import EventActivity, EventTeam, EventTag, School, Season, Summary, Team
from .EventManagement import EventManagementView
from panel.component.CustomElements import Table
from misc.CustomFunctions import MiscFunctions, RequestFunctions, LogFunctions


class EventView(EventManagementView):
    def __init__(self, request):
        super().__init__(request)
        self.validation_table = {
            'base_table_invalid': {'_state', 'event_rotation_detail'},
            'base_form_invalid': {'_state', 'id', 'event_school_ids', 'event_team_number', 'event_create_time'},
        }
        
        self.assoc_class_activity = EventActivity
        self.assoc_class_team = Team
        self.assoc_class_school = School
        self.assoc_class_team_link = EventTeam
        self.assoc_class_tag = EventTag
        self.assoc_class_summary = Summary
        self.assoc_class_season = Season

        self.event_race_tag = ["Fleet A", "Fleet B"]
        self.event_team_name_suffix = ["Team A", "Team B"]
        self.event_activity_type = "race"

    def setFormPath(self):
        return 'all'

    def getTableHeader(self):
        return self.getTableSpecificHeader() + ["edit"]  # don't have delete in header

    def getTableRow(self, content):
        rowContent = dict()
        rowContent["db_content"] = self.getTableRowContent(content)
        rowContent["button"] = [self.makeEditDeleteBtn('custom', str(content.id))[0]]  # no delete button
        return rowContent

    def grabTableData(self, form_path):
        tableHeader = self.getTableHeader()
        tableContent = self.getTableContent(self.getRangeTerms(), **self.getFilterTerms())
        table = Table(self.base_class, form_path).buildTable(tableHeader, tableContent)
        return [table]

    def abstractFormProcess(self, action, **kwargs):
        try:
            if not action == 'edit':
                raise Exception('Trying to ' + action + ' event in Logic-less Event Data Management Panel')

            post_dict = dict(self.request.POST)

            event_type = RequestFunctions.getSingleRequestObj(post_dict, 'event_type')
            event_name = RequestFunctions.getSingleRequestObj(post_dict, 'event_name')
            event_status = RequestFunctions.getSingleRequestObj(post_dict, 'event_status')
            event_description = RequestFunctions.getSingleRequestObj(post_dict, 'event_description')
            event_location = RequestFunctions.getSingleRequestObj(post_dict, 'event_location')
            event_season = RequestFunctions.getSingleRequestObj(post_dict, 'event_season')
            event_region = RequestFunctions.getSingleRequestObj(post_dict, 'event_region')
            event_host = RequestFunctions.getSingleRequestObj(post_dict, 'event_host')
            event_school = RequestFunctions.getMultipleRequestObj(post_dict, 'event_team')
            event_race_number = RequestFunctions.getSingleRequestObj(post_dict, 'event_race_number')
            event_boat_rotation_name = RequestFunctions.getSingleRequestObj(post_dict, 'event_boat_rotation_name')
            event_rotation_detail = MiscFunctions.jsonLoadCatch(
                RequestFunctions.getSingleRequestObj(post_dict, 'event_rotation_detail'))
            event_start_date = RequestFunctions.getSingleRequestObj(post_dict, 'event_start_date')
            event_end_date = RequestFunctions.getSingleRequestObj(post_dict, 'event_end_date')

            dispatcher = super().populateDispatcher()
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None)
                event_creation = self.useAPI(self.base_class).editSelf(id=event_creation_id)
            else:
                event_creation = self.base_class()

            # event generation
            event_creation.event_type = int(event_type)
            event_creation.event_name = event_name
            event_creation.event_status = event_status
            event_creation.event_description = event_description
            event_creation.event_location = event_location
            event_creation.event_season = int(event_season)
            event_creation.event_region = int(event_region)
            event_creation.event_host = int(event_host)
            event_creation.event_race_number = int(event_race_number)
            event_creation.event_boat_rotation_name = event_boat_rotation_name
            event_creation.event_start_date = event_start_date
            event_creation.event_end_date = event_end_date
            event_creation.event_team_number = 0 if event_school is None else len(event_school)
            event_creation.event_school_ids = [] if event_school is None else event_school
            event_creation.event_rotation_detail = event_rotation_detail
            event_creation.save()

            if not action == 'edit':
                event_creation.save()

            LogFunctions.generateLog(
                self.request, 'admin', LogFunctions.makeLogQuery(
                    self.base_class, action.title(), id=event_creation.id)
            )

        except Exception as e:
            print({"Error": "Cannot Process " + action.title() + " Request."})
            print(e)
