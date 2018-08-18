from abc import ABC, abstractmethod
from misc.GeneralFunctions import generalFunctions as gf

class AbstractAPI(ABC):
    def __init__(self, request):
        self.request = request;
        self.auth = self.request['auth'];
        self.base = self.setBaseClass();

    @abstractmethod
    def setBaseClass(self):
        pass;

    @abstractmethod
    def authenticate(self):
        pass;
