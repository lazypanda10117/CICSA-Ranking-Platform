from abc import abstractmethod
from django.shortcuts import redirect
from django.urls import reverse

from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class CoreDataProcess(AbstractBaseProcess):
    def __init__(self, request, param):
        super().__init__(request, param)
        self.app_name = self._setAppName()
        self.view_dispatcher = self._setViewDispatcher()

    @abstractmethod
    def _setAppName(self):
        pass

    @abstractmethod
    def _setViewDispatcher(self):
        pass

    def process(self):
        route = self.param.get('route')
        action = self.request.GET.get("action")
        element_id = self.request.GET.get("element_id")
        route_wrapper = self.view_dispatcher.get(route)
        route_class = route_wrapper.routeClass(self.request)
        route_class(self.request).processData(action=action, element_id=element_id)
        return redirect(self.__getViewDestination())

    def parseParams(self, param):
        super().parseMatch('[\w|\d]+')
        param = dict(route=param)
        return param

    # Util Functions
    def __getViewDestination(self):
        return reverse(
            'panel.module.{}.view_dispatch_param'.format(self.app_name),
            args=['data', self.param.get('route')]
        )
