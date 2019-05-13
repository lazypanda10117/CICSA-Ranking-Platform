from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from ..base.block.Base import AbstractBlockApp
from .CustomView import CustomView
from .GeneralView import GeneralView


def index(request):
    return ManagementDataView().authenticateModule(
        request,
        ManagementDataView().home())


@csrf_exempt
def viewDispatch(request, param, route):
    dispatcher = ManagementDataView().setViewDispatcher()
    view = dispatcher.get(route)(request)
    return ManagementDataView().authenticateModule(
        request,
        view.dispatch(param))


class ManagementDataView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    def getBaseAppName(self):
        return "DataModule"

    def home(self):
        return super().index('panel.module.management_data.view_dispatch_param', ['event', 'custom'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('general', GeneralView)
        dispatcher.add('custom', CustomView)
        return dispatcher

    def setProcessDispatcher(self):
        pass
