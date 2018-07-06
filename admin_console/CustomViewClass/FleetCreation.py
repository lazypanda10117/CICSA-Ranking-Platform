from ..HelperClass import *
from ..generalFunctions import *
from .EventCreationView import *

from ..models import *


class FleetCreationView(EventCreationView):
    def abstractFormProcess(self, action, **kwargs):
        def add():
            event_creation = self.base_class();

        def edit(key):
            event_creation = self.base_class.objects.get(id=key);
            pass;

        def delete(key):
            event_creation = self.base_class.objects.get(id=key);
            pass;

        post_dict = dict(self.request.POST);

        event_type = getPostObj(self.post_dict, 'event_creation_event_type');
        event_name = getPostObj(self.post_dict, 'event_creation_event_name');
        event_status = getPostObj(self.post_dict, 'event_creation_event_status');
        event_description = getPostObj(self.post_dict, 'event_creation_event_description');
        event_location = getPostObj(self.post_dict, 'event_creation_event_location');
        event_region = getPostObj(self.post_dict, 'event_creation_event_region');
        event_host = getPostObj(self.post_dict, 'event_creation_event_host');
        event_team = getPostObj(self.post_dict, 'event_creation_event_team');
        event_num_race = getPostObj(self.post_dict, 'event_creation_event_num_race');
        event_num_boat = getPostObj(self.post_dict, 'event_creation_event_num_boat');
        event_start_date = getPostObj(self.post_dict, 'event_creation_event_start_date');
        event_end_date = getPostObj(self.post_dict, 'event_creation_event_end_date');

        try:
            dispatcher = super().populateDispatcher();
            if dispatcher.get(action):
                event_creation_id = kwargs.pop('id', None);
                if action == 'edit':
                    edit(event_creation_id);
                elif action == 'delete':
                    delete(event_creation_id);
            else:
                if action == 'add':
                    add();
        except:
            print({"Error": "Cannot Process " + action.title() + " Request." });