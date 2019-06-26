from django.views.decorators.csrf import csrf_exempt
from misc.CustomElements import Dispatcher
from ..base.block.Base import AbstractBlockApp
from .CustomPages import LeagueRankingPage, EventActivityPage, EventActivityDetailPage, EventChoicePage
from .CustomProcesses import EventChoiceProcess
from panel.module.ModuleRegistry import ModuleRegistry


def index(request):
    return ManagementEventView().authenticateModule(
        request,
        ManagementEventView().home())


def viewDispatch(request, route, param=''):
    return ManagementEventView().authenticateModule(
        request,
        ManagementEventView().viewDispatch(request, route, param))


@csrf_exempt
def processDispatch(request, route, param=''):
    return ManagementEventView().authenticateModule(
        request,
        ManagementEventView().processDispatch(request, route, param))


class ManagementEventView(AbstractBlockApp.AppView):
    # Block App Base View Inherited Functions
    def getBaseAppName(self):
        return ModuleRegistry.MANAGEMENT_EVENT

    def home(self):
        return super().index('panel.module.management_event.view_dispatch', ['choice'])

    def setViewDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('choice', EventChoicePage)
        dispatcher.add('event', LeagueRankingPage)
        dispatcher.add('activity', EventActivityPage)
        dispatcher.add('activity detail', EventActivityDetailPage)
        return dispatcher

    def setProcessDispatcher(self):
        dispatcher = Dispatcher()
        dispatcher.add('choice', EventChoiceProcess)
        return dispatcher
