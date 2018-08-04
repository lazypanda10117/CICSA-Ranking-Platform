from abc import abstractmethod, ABC
from admin_console.generalFunctions import *

class AbstractDisplayClass(ABC):
    def __init__(self, request, param):
        self.request = request;
        self.param = param;

    def renderHelper(self, title, element_list):
        return kickRequest(self.request, True, render(
            self.request, 'event_management/eventDisplayList.html',
            {'title': title, 'element_list': element_list}));

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def generateList(self):
        pass;