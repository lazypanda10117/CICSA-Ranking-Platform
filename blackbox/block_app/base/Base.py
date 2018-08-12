from django.shortcuts import render, reverse, redirect
from abc import abstractmethod, ABC
from cicsa_ranking.models import *
from misc.GeneralFunctions import generalFunctions as gf
from misc.Dispatcher import Dispatcher

class AbstractBlockApp(ABC):
    class AppView():
        @abstractmethod
        def setViewDispatcher(self):
            pass;

        def index(self, request, path):
            return redirect(reverse(path));

        def viewDispatch(self, request, dispatch_path, param):
            dispatcher = self.setDispatcher();
            object = dispatcher.get(dispatch_path)(request, param);
            return object.render();
