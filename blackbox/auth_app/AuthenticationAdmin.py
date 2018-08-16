import cicsa_ranking.models as model
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