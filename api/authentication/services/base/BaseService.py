from abc import ABC

from misc.CustomElements import Dispatcher
from api.authentication import AuthenticationActionType

# Each service takes in a query object and returns a list of of objects
class BaseService(ABC):
    def __init__(self, request, objects):
        self.request = request
        self.objects = self.__inputTransformer(objects)
        self.raw_objects = self.objects
        self.service_dispatcher = self.__setServiceDispatcher()

    def __setServiceDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add(AuthenticationActionType.ADD, self._verifyADD)
        dispatcher.add(AuthenticationActionType.EDIT, self._verifyEDIT)
        dispatcher.add(AuthenticationActionType.DELETE, self._verifyDELETE)
        dispatcher.add(AuthenticationActionType.VIEW, self._verifyVIEW)
        return dispatcher

    # This transforms input to a list of objects (The standard for service inputs)
    def __inputTransformer(self, objects):
        if objects is None:
            return []
        elif type(objects) == 'QuerySet':
            return [obj for obj in objects]
        else:
            return [objects]

    def verify(self, identifier):
        if self.service_dispatcher.exists(identifier):
            return self.service_dispatcher.get(identifier)()
        else:
            return self._verifyOTHER(identifier)

    # The following functions are to be implemented by the respective services that inherit this.
    def _verifyADD(self):
        return self.objects

    def _verifyEDIT(self):
        return self.objects

    def _verifyDELETE(self):
        return self.objects

    def _verifyVIEW(self):
        return self.objects

    def _verifyOTHER(self, identifier):
        return None
