from abc import ABC, abstractmethod

from cicsa_ranking import ArchiveModel
from misc.CustomElements import Dispatcher


class AuthenticationComponentBase(ABC):
    def __init__(self, request):
        self.request = request
        self.base = self.setBaseModelClass()

    @staticmethod
    def isArchived(self, obj):
        return obj.__class__ in [ArchiveModel] and obj.archived

    # maybe addd a isHistory as well later?
    # def __isHistory(self, obj):

    @abstractmethod
    def setBaseModelClass(self):
        pass

    # This is only being called when passed in a none object. Essentially does nothing, just for completeness sake.
    class NoneAuthenticate:
        def __init__(self, objects):
            self.objects = objects

        def viewAuthenticate(self):
            return self.objects

        def editAuthenticate(self):
            return self.objects

        def addAuthenticate(self):
            return self.objects

        def deleteAuthenticate(self):
            return self.objects

    # This is called when you pass in a bulk object
    class BulkAuthenticate:
        def __init__(self, objects):
            self.objects = objects

        def viewAuthenticate(self):
            return self.objects

        # An example of filtering out archived object
        def editAuthenticate(self):
            return [o for o in self.objects if not AuthenticationComponentBase.isArchived(o)]

        def addAuthenticate(self):
            return []

        def deleteAuthenticate(self):
            return []

    class SingleAuthenticate:
        def __init__(self, objects):
            self.objects = objects

        def viewAuthenticate(self):
            return self.objects

        # Another example of how to restrict editing access
        def editAuthenticate(self):
            return self.objects if not AuthenticationComponentBase.isArchived(self.objects) else None

        def addAuthenticate(self):
            return self.objects

        def deleteAuthenticate(self):
            return self.objects

    def authTypeDispatcher(self, objects):
        if objects is None:
            return self.NoneAuthenticate(objects)
        elif type(objects) == 'QuerySet':
            return self.BulkAuthenticate(objects)
        else:
            return self.SingleAuthenticate(objects)

    def getAuthDispatcher(self, objects):
        dispatcher = Dispatcher()
        dispatcher.add('view', self.authTypeDispatcher(objects).viewAuthenticate())
        dispatcher.add('add', self.authTypeDispatcher(objects).addAuthenticate())
        dispatcher.add('edit', self.authTypeDispatcher(objects).editAuthenticate())
        dispatcher.add('delete', self.authTypeDispatcher(objects).deleteAuthenticate())
        return dispatcher

    def authenticate(self, route, objects):
        return self.getAuthDispatcher(objects).get(route)
