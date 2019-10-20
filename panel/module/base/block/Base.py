from django.shortcuts import redirect
from django.shortcuts import reverse
from abc import ABC
from abc import abstractmethod

from misc.CustomFunctions import MiscFunctions
from panel.module_permission import ModulePermission


class AbstractBlockApp(ABC):
    class AppView:
        @abstractmethod
        def getBaseAppName(self):
            pass

        @abstractmethod
        def setViewDispatcher(self):
            pass

        @abstractmethod
        def setProcessDispatcher(self):
            pass

        def __authenticateModule(self, request, callback=None, failure=None):
            return ModulePermission(request).verifyRequest(self.getBaseAppName(), callback, failure)

        def index(self, request, path, args=None):
            args = [] if args is None else args
            return self.__authenticateModule(request=request, callback=(lambda: redirect(reverse(path, args=args))))

        def viewDispatch(self, request, dispatch_path, param=''):
            page = self.setViewDispatcher().get(dispatch_path)(request, param)
            return self.__authenticateModule(
                request=request,
                callback=lambda: page.render()
            )

        def processDispatch(self, request, dispatch_path, param=''):
            page = self.setProcessDispatcher().get(dispatch_path)(request, param)
            return self.__authenticateModule(
                request=request,
                callback=lambda: page.process(),
                failure=lambda: MiscFunctions.lraise(Exception("Insufficient Permission to Access Module Process"))
            )
