from abc import ABC, abstractmethod
from ..generalFunctions import *

class API(ABC):
    def __init__(self, request):
        self.request = request;

    def authenitication(self):
        return signed_in(self.request, 'admin');
