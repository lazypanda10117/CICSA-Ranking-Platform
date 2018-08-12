from django.shortcuts import render, reverse, redirect
from abc import abstractmethod, ABC
from misc.GeneralFunctions import generalFunctions as gf

class AbstractBasePage(ABC):
    def __init__(self, request, param, page_path):
        self.request = request;
        self.param = param;
        self.page_path = page_path;

    def renderHelper(self, page_object):
        return gf.kickRequest(self.request, True, render(self.request, self.page_path, page_object));

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def generateList(self):
        pass;