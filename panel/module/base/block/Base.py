from django.shortcuts import reverse, redirect
from abc import abstractmethod, ABC


class AbstractBlockApp(ABC):
    class AppView:
        @abstractmethod
        def setViewDispatcher(self):
            pass

        @abstractmethod
        def setProcessDispatcher(self):
            pass

        @staticmethod
        def index(path, args=None):
            args = [] if args is None else args
            return redirect(reverse(path, args=args))

        def viewDispatch(self, request, dispatch_path, param=''):
            dispatcher = self.setViewDispatcher()
            page = dispatcher.get(dispatch_path)(request, param)
            return page.render()

        def processDispatch(self, request, dispatch_path, param=''):
            dispatcher = self.setProcessDispatcher()
            page = dispatcher.get(dispatch_path)(request, param)
            return page.process()
