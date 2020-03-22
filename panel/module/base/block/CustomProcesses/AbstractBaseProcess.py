import re
from django.http import Http404
from abc import abstractmethod, ABC


class AbstractBaseProcess(ABC):
    def __init__(self, request, param):
        self.request = request
        self.raw_param = param
        self.param = self.parseParams(self.raw_param)
        self.post_data = self.__parseRequestPost(self.request)

    def __parseRequestPost(self, request):
        EXCLUDED_FIELDS = ['csrfmiddlewaretoken']
        result = dict(request.POST)
        for field in EXCLUDED_FIELDS:
            result.pop(field)
        return result

    def parseMatch(self, pattern):
        match = re.match(pattern, self.raw_param)
        if match:
            return match
        else:
            raise Http404

    @abstractmethod
    def parseParams(self, param):
        pass

    @abstractmethod
    def process(self):
        pass
