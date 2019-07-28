import re
from django.shortcuts import render
from django.http import Http404
from abc import abstractmethod, ABC

from api.authentication import AuthenticationGuardType


class AbstractBasePage(ABC):
    def __init__(self, request, param):
        self.request = request
        self.raw_param = param
        self.param = self.parseParams(self.raw_param)
        self.page_path = self.getPagePath()
        self.guard_type = self.getGuardType()

    def getGuardType(self):
        return AuthenticationGuardType.ADMIN_TEAM_GUARD

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def parseParams(self, param):
        pass

    def parseMatch(self, pattern):
        match = re.match(pattern, self.raw_param)
        if match:
            return match
        else:
            raise Exception("Page parameters parsing engine failed to recognize provided path")

    @staticmethod
    def getPagePath():
        return 'platform/module/base/block/displayList.html'

    def renderHelper(self, page_object):
        return render(self.request, self.page_path, dict(page=page_object))
