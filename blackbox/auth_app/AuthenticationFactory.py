import misc
import blackbox.auth_app

class AuthenticaitonFactory():
    def __init__(self, path):
        self.path = path;

    def getDispatcher(self):
        dispatcher = misc.Dispatcher.Dispatcher();
        dispatcher.add('admin', blackbox.auth_app.AuthenticationAdmin);
        dispatcher.add('team', blackbox.auth_app.AuthenticationTeam);
        dispatcher.add('public', blackbox.auth_app.AuthenticationPublic);
        return dispatcher;

    def dispatch(self):
        return self.getDispatcher().get(self.path);


