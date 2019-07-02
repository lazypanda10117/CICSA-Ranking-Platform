from abc import ABC

from misc.CustomElements import Dispatcher
from api.authentication import AuthenticationActionType


class BaseService(ABC):
    def __init__(self, request, objects):
        self.request = request
        self.objects = objects
        self.service_dispatcher = self.__setServiceDispatcher()

    def __setServiceDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(AuthenticationActionType.ADD, self._verifyADD)
        dispatcher.add(AuthenticationActionType.EDIT, self._verifyEDIT)
        dispatcher.add(AuthenticationActionType.DELETE, self._verifyDELETE)
        dispatcher.add(AuthenticationActionType.VIEW, self._verifyVIEW)
        return dispatcher

    # This return transformed needs to be used for all objects return for compatibility issues
    def _returnTransformer(self, response):
        if len(response) == 0:
            return None
        elif len(response) == 1:
            return response[0]
        else:
            return response

    def verify(self, identifier):
        if self.service_dispatcher.exists(identifier):
            return self.service_dispatcher.get(identifier)()
        else:
            return self._verifyOTHER()

    # The following functions are to be implemented by the respective services that inherit this.
    def _verifyADD(self):
        return self._returnTransformer(self.objects)

    def _verifyEDIT(self):
        return self._returnTransformer(self.objects)

    def _verifyDELETE(self):
        return self._returnTransformer(self.objects)

    def _verifyVIEW(self):
        return self._returnTransformer(self.objects)

    def _verifyOTHER(self):
        return None