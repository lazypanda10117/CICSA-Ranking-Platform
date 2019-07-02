from abc import ABC, abstractmethod

from api.authentication.services import ArchiveService
from api.authentication import AuthenticationActionType
from misc.CustomElements import Dispatcher


class AuthenticationComponentBase(ABC):
    def __init__(self, request):
        self.request = request
        self.base = self.setBaseModelClass()

    @abstractmethod
    def setBaseModelClass(self):
        pass

    # This is only being called when passed in a none object. Essentially does nothing, just for completeness sake.
    class NoneAuthenticate:
        def __init__(self, request, objects):
            self.request = request
            self.objects = objects

        def viewAuthenticate(self):
            return None

        def editAuthenticate(self):
            return None

        def addAuthenticate(self):
            return None

        def deleteAuthenticate(self):
            return None

    # This is called when you pass in a bulk object
    class BulkAuthenticate:
        def __init__(self, request, objects):
            self.request = request
            self.objects = objects

        def viewAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.VIEW)
            return response

        # An example of filtering out archived object
        def editAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.EDIT)
            return response

        def addAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.ADD)
            return response

        def deleteAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.DELETE)
            return response

    class SingleAuthenticate:
        def __init__(self, request, objects):
            self.request = request
            self.objects = objects

        def viewAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.VIEW)
            return response

        # Another example of how to restrict editing access
        def editAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.EDIT)
            # say maybe later you have a history service, then you do
            # response = HistoryService(self.request, response).verify(AuthenticationActionType.EDIT)
            return response

        def addAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.ADD)
            return response

        def deleteAuthenticate(self):
            response = ArchiveService(self.request, self.objects).verify(AuthenticationActionType.DELETE)
            return response

    def authTypeDispatcher(self, objects):
        if objects is None:
            return self.NoneAuthenticate(objects)
        elif type(objects) == 'QuerySet':
            return self.BulkAuthenticate(objects)
        else:
            return self.SingleAuthenticate(objects)

    def getAuthDispatcher(self, objects):
        dispatcher = Dispatcher()
        dispatcher.add(AuthenticationActionType.VIEW, self.authTypeDispatcher(objects).viewAuthenticate())
        dispatcher.add(AuthenticationActionType.ADD, self.authTypeDispatcher(objects).addAuthenticate())
        dispatcher.add(AuthenticationActionType.EDIT, self.authTypeDispatcher(objects).editAuthenticate())
        dispatcher.add(AuthenticationActionType.DELETE, self.authTypeDispatcher(objects).deleteAuthenticate())
        return dispatcher

    def authenticate(self, route, objects):
        return self.getAuthDispatcher(objects).get(route)
