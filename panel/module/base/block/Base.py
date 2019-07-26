from django.shortcuts import reverse, redirect
from abc import abstractmethod, ABC

from api.authentication import AuthenticationGuard, AuthenticationGuardType
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

        def __authenticateRoute(self, request, guard_type):
            AuthenticationGuard(guard_type, request).guard()

        def index(self, request, path, args=None):
            args = [] if args is None else args
            return self.__authenticateModule(request=request, callback=redirect(reverse(path, args=args)))

        def viewDispatch(self, request, dispatch_path, param=''):
            self.__authenticateModule(request=request)
            dispatcher = self.setViewDispatcher()
            page = dispatcher.get(dispatch_path)(request, param)
            self.__authenticateRoute(request, page.getGuardType())
            return page.render()

        def processDispatch(self, request, dispatch_path, param=''):
            self.__authenticateModule(
                request=request,
                failure=Exception("Insufficient Permission to Access Module Process")
            )
            dispatcher = self.setProcessDispatcher()
            page = dispatcher.get(dispatch_path)(request, param)
            self.__authenticateRoute(request, page.getGuardType())
            return page.process()
