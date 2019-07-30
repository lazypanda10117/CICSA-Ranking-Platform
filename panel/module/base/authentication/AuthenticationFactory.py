from api.authentication import AuthenticationType
from misc.CustomElements import Dispatcher
from panel.module.base.authentication import AuthenticationAdmin, AuthenticationTeam


class AuthenticationFactory:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def getDispatcher():
        dispatcher = Dispatcher()
        dispatcher.add(AuthenticationType.ADMIN, AuthenticationAdmin)
        dispatcher.add(AuthenticationType.TEAM, AuthenticationTeam)
        dispatcher.add(AuthenticationType.PUBLIC, AuthenticationTeam)
        return dispatcher

    def dispatch(self):
        return self.getDispatcher().get(self.path)
