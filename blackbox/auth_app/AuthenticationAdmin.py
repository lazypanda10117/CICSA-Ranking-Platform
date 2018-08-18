from cicsa_ranking import models as model
from blackbox import api
from misc.Dispatcher import Dispatcher
from .AuthenticantionComponentBase import AuthenticationComponentBase

class AuthenticationAdmin():
    def __init__(self, request):
        self.request = request;

    def getDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        dispatcher.add(model.EventActivity.__class__.__name__, self.EventActivity);
        return dispatcher;

    def dispatch(self, key):
        dispatcher = self.getDispatcher();
        return dispatcher.get(key);

    class EventActivity(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventActivity;

    class EventActivity(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventActivity;

    class EventActivity(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventActivity;