from api.authentication import AuthenticationGuardType
from api.base import AbstractCoreAPI
from misc.CustomFunctions import RequestFunctions
from misc.CustomFunctions import MiscFunctions


class SessionAPI(AbstractCoreAPI):
    def __init__(self, request):
        super().__init__(request=request, permission=AuthenticationGuardType.PUBLIC_GUARD)

    def getPanelConfig(self, key):
        panel_config = RequestFunctions.sessionGetter(self.request, "panel_config")
        return MiscFunctions.noneCatcher(key, panel_config)

    def getClientConfig(self, key):
        client_config = RequestFunctions.sessionGetter(self.request, "client_config")
        return MiscFunctions.noneCatcher(key, client_config)
