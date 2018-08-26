from abc import ABC, abstractmethod
from misc.CustomElements import Dispatcher

class AuthenticationComponentBase(ABC):
    def __init__(self, request):
        self.request = request;
        self.base = self.setBaseModelClass();

    @abstractmethod
    def setBaseModelClass(self):
        pass;

    class NoneAuthenticate():
        def __init__(self, objects):
            self.objects = objects;

        def viewAuthenticate(self):
            return self.objects;

        def editAuthenticate(self):
            return self.objects;

        def addAuthenticate(self):
            return self.objects;

        def deleteAuthenticate(self):
            return self.objects;

    class BulkAuthenticate():
        def __init__(self, objects):
            self.objects = objects;

        def viewAuthenticate(self):
            return self.objects;

        def editAuthenticate(self):
            return [];

        def addAuthenticate(self):
            return self.editAuthenticate();

        def deleteAuthenticate(self):
            return self.editAuthenticate();

    class SingleAuthenticate():
        def __init__(self, objects):
            self.objects = objects;

        def viewAuthenticate(self):
            return self.objects;

        def editAuthenticate(self):
            return self.objects;

        def addAuthenticate(self):
            return self.editAuthenticate();

        def deleteAuthenticate(self):
            return self.editAuthenticate();

    def authTypeDispatcher(self, objects):
        if len(objects) == 0:
            return self.NoneAuthenticate(objects);
        elif len(objects) == 1:
            return self.SingleAuthenticate(objects);
        else:
            return self.BulkAuthenticate(objects);

    def getAuthDispatcher(self, objects):
        dispatcher = Dispatcher();
        dispatcher.add('view', self.authTypeDispatcher(objects).viewAuthenticate());
        dispatcher.add('add', self.authTypeDispatcher(objects).addAuthenticate());
        dispatcher.add('edit', self.authTypeDispatcher(objects).editAuthenticate());
        dispatcher.add('delete', self.authTypeDispatcher(objects).deleteAuthenticate());
        return dispatcher;

    def authenticate(self, route, objects):
        return self.getAuthDispatcher(objects).get(route);