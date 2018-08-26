import misc
from blackbox.auth_app import AuthenticationPublic, AuthenticationTeam, AuthenticationAdmin

class AuthenticaitonFactory():
    def __init__(self, path):
        self.path = path;

    def getDispatcher(self):
        dispatcher = misc.Dispatcher.Dispatcher();
        dispatcher.add('admin', AuthenticationAdmin);
        dispatcher.add('team', AuthenticationTeam);
        dispatcher.add('public', AuthenticationPublic);
        return dispatcher;

    def dispatch(self):
        return self.getDispatcher().get(self.path);


