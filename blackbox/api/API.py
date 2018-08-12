from abc import ABC, abstractmethod
from misc.GeneralFunctions import generalFunctions as gf

class API(ABC):
    def __init__(self, request):
        self.request = request;

    def authenitication(self):
        return gf.signed_in(self.request, 'admin');
