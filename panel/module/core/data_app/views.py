from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from panel.module.base.block.Base import AbstractBlockApp
from panel.module.core.data_app.CoreProcesses import CoreDataProcess
from panel.module.core.data_app.CoreViews import CoreDataView
from panel.module.ModuleRegistry import ModuleRegistry


def index(request):
    return CoreDataApp().home(request)


def viewDispatch(request, route, param=''):
    return CoreDataApp().viewDispatch(request, route, param)


@csrf_exempt
def processDispatch(request, route, param=''):
    return CoreDataApp().processDispatch(request, route, param)


class CoreDataApp(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    def getBaseAppName(self):
        return ModuleRegistry.CORE_DATA

    def home(self, request):
        return super().index(request, 'panel.module.core.data_app.view_dispatch', ['data'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('data', CoreDataView)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('data', CoreDataProcess)
        return dispatcher
