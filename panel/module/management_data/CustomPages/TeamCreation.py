from ..HelperClass import *
from ..generalFunctions import *
from .EventManagement import *

from ..models import *


class TeamManagementView(EventManagementView):
    def __init__(self, request):
        self.event_type = 'team race';
        super().__init__(request);

    def getChoiceData(self):
        choice_data = super().getChoiceData();
        choice_data['event_type'] = tuple([(lambda x: (x.id, x.event_type_name))
                                           (getModelObject(EventType, event_type_name=self.event_type))]);
        return choice_data;

    def setFormPath(self):
        return self.event_type;

    def _add(self):
        pass;

    def _edit(self, key):
        pass;

    def _delete(self, key):
        pass;

    def abstractFormProcess(self, action, **kwargs):
        self.post_dict = dict(self.request.POST);
        try:
            dispatcher = super().populateDispatcher();
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None);
                if action == 'edit':
                    self._edit(event_creation_id);
                elif action == 'delete':
                    self._delete(event_creation_id);
            else:
                if action == 'add':
                    self._add();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request." });

    def getDBMap(self, data):
        return None;