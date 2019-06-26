from api.base import AbstractCoreAPI
from misc.CustomFunctions import RequestFunctions
from misc.CustomFunctions import MiscFunctions


class SessionAPI(AbstractCoreAPI):
    def getPanelConfig(self, key):
        panel_config = RequestFunctions.sessionGetter(self.request, "panel_config")
        return MiscFunctions.noneCatcher(key, panel_config)
