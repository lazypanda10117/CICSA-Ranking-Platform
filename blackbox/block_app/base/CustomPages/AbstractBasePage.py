import re
from django.shortcuts import render, reverse, redirect
from django.http import Http404
from abc import abstractmethod, ABC
from misc.GeneralFunctions import generalFunctions as gf

class AbstractBasePage(ABC):
    def __init__(self, request, param):
        self.request = request;
        self.param = param;
        self.page_path = self.getPagePath();

    @abstractmethod
    def render(self):
        pass;

    @abstractmethod
    def parseParams(self, param):
        pass;

    @abstractmethod
    def setBaseUrl(self):
        pass;

    def parseMatch(self, pattern):
        match = re.match(pattern, self.param);
        if match:
            return match;
        else:
            raise Http404;

    def getPagePath(self):
        return 'blackbox/block_app/base/sth.html';

    def renderHelper(self, page_object):
        return gf.kickRequest(self.request, True, render(self.request, self.page_path, page_object));


