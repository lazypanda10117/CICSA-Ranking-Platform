from abc import ABC, abstractmethod
from misc.GeneralFunctions import generalFunctions as gf

class AbstractAPI(ABC):
    def __init__(self, request):
        self.request = request;
        self.base = self.setBaseClass();

    @abstractmethod
    def setBaseClass(self):
        pass;

    def authenitication(self):
        return gf.signed_in(self.request, 'admin');
