from ..HelperClass import *
from ..generalFunctions import *
from .EventCreationView import *

from ..models import *


class GroupCreationView(EventCreationView):
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
