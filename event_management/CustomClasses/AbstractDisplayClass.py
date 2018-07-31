from abc import abstractmethod, ABC

class AbstractDisplayClass(ABC):
    def __init__(self, request, param):
        self.request = request;
        self.param = param;

    @abstractmethod
    def render(self):
        pass;

    @abstractmethod
    def generateList(self):
        pass;