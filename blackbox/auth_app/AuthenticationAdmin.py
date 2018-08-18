from cicsa_ranking import models as model
from blackbox import api
from .AuthenticantionComponentBase import AuthenticationComponentBase

class AuthenticationAdmin():
    def __init__(self, request):
        self.request = request;

    class EventActivity(AuthenticationComponentBase):
        def setBaseModelClass(self):
            return model.EventActivity;

        def viewAuthenticate(self):
            self.editAuthenticate();

        def editAuthenticate(self):
            self.identifier