from misc.CustomElements import Dispatcher
from panel.module.base.authentication import AuthenticationAdmin, AuthenticationTeam


class AuthenticationFactory:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def getDispatcher():
        dispatcher = Dispatcher()
        dispatcher.add('admin', AuthenticationAdmin)
        dispatcher.add('team', AuthenticationTeam)
        return dispatcher

    def dispatch(self):
        return self.getDispatcher().get(self.path)
