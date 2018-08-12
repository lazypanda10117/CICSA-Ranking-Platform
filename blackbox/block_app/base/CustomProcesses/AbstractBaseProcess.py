from django.shortcuts import render, reverse, redirect
from django.http import Http404
import re
from abc import abstractmethod, ABC
from misc.GeneralFunctions import generalFunctions as gf

class AbstractBaseProcess(ABC):
    def __init__(self, request, param):
        self.request = request;
        self.param = self.parseParams(param);

    def parseMatch(self, pattern):
        match = re.match(pattern, self.param);
        if match:
            return match;
        else:
            raise Http404;

    @abstractmethod
    def parseParams(self, param):
        pass;

    @abstractmethod
    def process(self):
        pass;