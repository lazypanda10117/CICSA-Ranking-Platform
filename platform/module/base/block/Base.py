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

        @abstractmethod
        def setProcessDispatcher(self):
            pass;

        def index(self, request, path, args=[]):
            return redirect(reverse(path, args=args));

        def viewDispatch(self, request, dispatch_path, param=''):
            dispatcher = self.setViewDispatcher();
            object = dispatcher.get(dispatch_path)(request, param);
            return object.render();

        def processDispatch(self, request, dispatch_path, param=''):
            dispatcher = self.setProcessDispatcher();
            object = dispatcher.get(dispatch_path)(request, param);
            return object.process();