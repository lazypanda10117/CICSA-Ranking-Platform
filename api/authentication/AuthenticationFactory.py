from misc.CustomElements import Dispatcher
from ..authentication import AuthenticationAdmin, AuthenticationTeam, AuthenticationPublic


class AuthenticationFactory:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def getDispatcher():
        dispatcher = Dispatcher();
        dispatcher.add('admin', AuthenticationAdmin)
        dispatcher.add('team', AuthenticationTeam)
        dispatcher.add('public', AuthenticationPublic)
        dispatcher.add(None, AuthenticationPublic)
        return dispatcher

    def dispatch(self):
        return self.getDispatcher().get(self.path)
