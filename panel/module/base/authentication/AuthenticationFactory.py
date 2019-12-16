from api.authentication import AuthenticationType
from misc.CustomElements import Dispatcher
from api.authentication import AuthenticationType
from panel.module.base.authentication import AuthenticationAdmin
from panel.module.base.authentication import AuthenticationPublic
from panel.module.base.authentication import AuthenticationTeam


class AuthenticationFactory:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def getDispatcher():
        dispatcher = Dispatcher()
        dispatcher.add(AuthenticationType.ADMIN, AuthenticationAdmin)
        dispatcher.add(AuthenticationType.TEAM, AuthenticationTeam)
        dispatcher.add(AuthenticationType.PUBLIC, AuthenticationPublic)
        return dispatcher

    def dispatch(self):
        return self.getDispatcher().get(self.path)
