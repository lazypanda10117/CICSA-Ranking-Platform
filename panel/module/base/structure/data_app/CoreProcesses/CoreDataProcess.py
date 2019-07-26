from abc import abstractmethod
from django.shortcuts import redirect
from django.urls import reverse

from misc.CustomElements import Dispatcher
from panel.module.base.block.CustomProcesses import AbstractBaseProcess


class CoreDataProcess(AbstractBaseProcess):
    def __init__(self, request, param):
        super().__init__(request, param)
        self.app_name = self._setAppName()
        self.view_dispatcher = self._setViewDispatcher()
        self.function_dispatcher = self._setFunctionDispatcher()

    @abstractmethod
    def _setAppName(self):
        pass

    @abstractmethod
    def _setViewDispatcher(self):
        pass

    def _setFunctionDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('add', self.add)
        dispatcher.add('edit', self.edit)
        dispatcher.add('delete', self.delete)
        return dispatcher

    # CRUD calls to specific data app pages
    def add(self, route_class, element_id):
        route_class(self.request).add()

    def edit(self, route_class, element_id):
        route_class(self.request).edit(element_id)

    def delete(self, route_class, element_id):
        route_class(self.request).delete(element_id)

    def process(self):
        route = self.param.get('route')
        action = self.request.GET.get("action")
        element_id = self.request.GET.get("element_id")
        route_wrapper = self.view_dispatcher.get(route)
        route_class = route_wrapper.routeClass(self.request)
        self.function_dispatcher.get(action)(
            route_class=route_class,
            element_id=element_id
        )
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
