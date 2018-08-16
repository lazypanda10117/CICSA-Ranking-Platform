from abc import ABC, abstractmethod
from misc.Dispatcher import Dispatcher

class AuthenticationComponentBase(ABC):
    def __init__(self, request, identifier, route):
        self.request = request;
        self.identifier = identifier;
        self.route = route;
        self.base = self.setBaseModelClass();

    @abstractmethod
    def setBaseModelClass(self):
        pass;

    @abstractmethod
    def viewAuthenticate(self):
        pass;

    @abstractmethod
    def editAuthenticate(self):
        pass;

    def addAuthenticate(self):
        return self.editAuthenticate();

    def deleteAuthenticate(self):
        return self.editAuthenticate();

    def getDispatcher(self):
        dispatcher = Dispatcher();
        dispatcher.add('view', self.viewAuthenticate());
        dispatcher.add('add', self.addAuthenticate());
        dispatcher.add('edit', self.editAuthenticate());
        dispatcher.add('delete', self.deleteAuthenticate());
        return dispatcher;

    def verify(self):
        return self.getDispatcher().get(self.route);