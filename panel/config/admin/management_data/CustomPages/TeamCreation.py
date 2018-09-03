import random
from misc.CustomFunctions import LogFunctions, MiscFunctions, ModelFunctions, RequestFunctions
from .EventManagement import EventManagementView
from cicsa_ranking.models import EventActivity, Team, School, EventTeam, EventTag, EventType, Summary, Season


class TeamManagementView(EventManagementView):
    def __init__(self, request):
        self.event_type = 'team race'
        self.assoc_class_type = EventType

        super().__init__(request)

    # Class Specific Functions
    def getChoiceData(self):
        choice_data = super().getChoiceData()
        choice_data['event_type'] = tuple(
            [(lambda x: (x.id, x.event_type_name))
             (self.useAPI(self.assoc_class_type).getSelf(event_type_name=self.event_type))])
        return choice_data

    def setFormPath(self):
        return self.event_type

    def _add(self):
        pass

    def _edit(self, key):
        pass

    def _delete(self, key):
        pass

    def abstractFormProcess(self, action, **kwargs):
        post_dict = dict(self.request.POST)
        try:
            dispatcher = super().populateDispatcher()
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None)
                if action == 'edit':
                    self._edit(event_creation_id)
                elif action == 'delete':
                    self._delete(event_creation_id)
            else:
                if action == 'add':
                    self._add()
        except Exception:
            print({"Error": "Cannot Process " + action.title() + " Request."})

    def getDBMap(self, data):
        return None
